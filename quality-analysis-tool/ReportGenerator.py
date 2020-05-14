from service.analyzers.AuditLogSummaryAnalyzer import AuditLogSummaryAnalyzer
from service.analyzers.AuditLogCorrectnessAnalyzer import AuditLogCorrectnessReportAnalyzer
from service.analyzers.AuditLogsMisplacedValuesAnalyzer import AuditLogsMisplacedValuesAnalyzer
from service.analyzers.AuditLogInsightsAnalyzer import AuditLogInsightsAnalyzer
from service.AuditLogService import AuditLogService
from service.LookupService import LookupService
from service.processors.AuditLogPreProcessor import AuditLogPreProcessor
from service.ManagementService import ManagementService
from service.utils.ExcelWriter import ExcelClient
from service.utils.PackageUtil import  PackageUtil
from service.utils.NotificationClient import NotificationClient
from service.validators.rules.ValidationRules import get_rules, get_weights
import service.constant as constant
import configparser
import logging
from datetime import datetime
import sys
import os

Teams = []
Users = []
current_env = 'current-environment'


def generate(log_level= logging.INFO):
    # initialize logger
    logging.basicConfig(level=log_level)

    # initialize configuration
    logging.info("Reading Configuration ....")
    if len(sys.argv) < 2:
        logging.error('Pass command arguments.')
        return
    if sys.argv[1] is None:
        logging.error('Pass the Environment command argument.')
        return

    environment = sys.argv[1]

    logging.info("Loading Environment variables for env : " + environment)
    env = environment

    config_parser = configparser.ConfigParser()
    config_parser.read('config.ini', encoding=None)
    config = config_parser[env]

    logging.info("Loading Environment variables for env : " + config.name)

    load_users_teams = config_parser[current_env]['UPDATE_LOOKUP']

    # update user, team lookup data
    if load_users_teams == 'True':
        logging.info("Fetching Teams from Management Service .... ")
        teams = get_teams(config)
        logging.info("\t Fetching Users from Management Service .... ")
        logging.info("\t\t Updating Users, Teams to lookup file .... ")
        lookup_service = LookupService(config)
        lookup_service.update_teams_and_users(teams, constant.LOOKUP_FILE_NAME)

        logging.info("Finished loading Users and Teams from Management Service .... ")

    # fetch logs
    logging.info("Fetching Audit Logs from Service .... ")
    audit_logs = fetch_audit_logs(config)
    logging.info("Finished pulling Audit Logs .... ")

    # pre-process logs
    logging.info("Start Pre-Processing the Audit Logs .... ")
    audit_log_preprocessor = AuditLogPreProcessor()
    logging.info("Loading User, Team, Component, sub-Component and Action Attributes .... ")
    processed_logs_fixed_attr_dataset = AuditLogPreProcessor.pre_process_audit_logs(audit_log_preprocessor, config, audit_logs, True)
    processed_logs = AuditLogPreProcessor.pre_process_audit_logs(audit_log_preprocessor, config, audit_logs, False)

    # summary, scoring analysis
    rules, weights = get_rules_weights(config)

    logging.info("Analyzing the Audit logs ....")
    audit_ogs_misplaced_values_analyzer = AuditLogsMisplacedValuesAnalyzer()
    logging.info("\t Aggregating logs, Analyzing Correctness Pass 1....")
    misplaced_data = audit_ogs_misplaced_values_analyzer.generate(processed_logs_fixed_attr_dataset)

    logging.info("\t\t Analyzing ......................................")
    audit_log_correctness_analyzer = AuditLogCorrectnessReportAnalyzer(rules, weights)
    logging.info("\t\t\t Aggregating logs, Analyzing Correctness Pass 2....")
    correctness_data = audit_log_correctness_analyzer.generate(processed_logs)

    logging.info("\t\t\t\t Consolidating records ....")
    audit_log_summary_generator = AuditLogSummaryAnalyzer(rules, weights)
    scoring_data = AuditLogSummaryAnalyzer.generate(audit_log_summary_generator, processed_logs)

    # writing to reports
    excel_client = ExcelClient()

    file_directory = os.path.dirname(os.path.realpath('__file__'))

    summary_data = [misplaced_data, correctness_data]
    summary_data_merged = excel_client.merge_dfs(summary_data)

    records = []
    records.append({'data': summary_data_merged, 'sheet_name': 'Summary_Report'})
    records.append({'data': scoring_data, 'sheet_name': 'Scoring_Analysis'})

    summary_report_output = os.path.join(file_directory, constant.REPORT_SUMMARY_FILE_NAME)

    ExcelClient.write_to_excel(excel_client, records,  summary_report_output)
    logging.info("\t\t\t\t\t Generating Summary Reports ....")

    # Insights Analysis
    logging.info("Analyzing the Audit logs for Insights ....")

    insights_report_output = os.path.join(file_directory, constant.REPORT_INSIGHTS_FILE_NAME)

    audit_log_insights_generator = AuditLogInsightsAnalyzer(rules, weights, insights_report_output)
    logging.info("\t\t Generating Insights for Reporting ....")
    AuditLogInsightsAnalyzer.generate(audit_log_insights_generator, processed_logs,)

    # package reports
    package_util = PackageUtil()

    report_directory = os.path.join(file_directory, constant.REPORT_DIRECTORY)
    dst_directory = 'output'
    report_name = str(datetime.utcnow()) + '_reports'

    package_util.zip_folder(report_directory, dst_directory, report_name)

    # post to slack channel
    notification_client = NotificationClient(url=config['SLACK_URL'],
                                             url_param=config['SLACK_URL_PARAM'],
                                             channel=config['SLACK_CHANNEL'],
                                             user_name=config['SLACK_USER'])

    notification_client.post_notification(summary_data.__str__().replace('{', ' ').replace('}', ' ').replace('[', ' ').replace(']', ' '))

    logging.info("done, View reports ....")


def fetch_audit_logs(config):

    headers = {'apikey': str(config['API_KEY']), 'username': str(config['API_USERNAME'])}

    ping_response, total_count = get_logs(config, 0, 10, headers)
    page_limit = int(config['API_PAGE_SIZE'])

    batch_size = (total_count/page_limit) + 1
    page_number = 1

    responses = []

    for batch in range(batch_size):
        page_response, total_count = get_logs(config, page_number, page_limit, headers)
        responses += page_response
        page_number += 1
        processed_records = total_count - (page_number*batch_size)
        logging.info(str(processed_records) + ' pending records to fetch.')

    return responses


def get_logs(config, page_number, page_limit, headers):

    body = {
        "query_list": [

            {"userId": str(config['API_USERNAME'])},
            {"offSet": page_number},
            {"limit": page_limit}
        ]
    }

    service = AuditLogService(str(config['AUDIT_LOG_SERVICE_HOST']), str(config['AUDIT_LOG_SERVICE_ROUTE']), headers, body)
    response = service.get_audit_logs_v2()
    return response['result'], response['total_rows']


def get_test_logs(config):
    lookup_service = LookupService(config)
    test_logs = lookup_service.get_content('mockdata.txt', 'result')

    return test_logs


def get_teams(config):
    headers = {'apikey': str(config['API_KEY']), 'username': str(config['API_USERNAME'])}

    management_service = ManagementService(str(config['MANAGEMENT_SERVICE_HOST']), (str(config['TEAM_MANAGEMENT_SERVICE_ROUTE'])), headers)
    teams = management_service.get_teams()

    return teams


def get_rules_weights(config):
    lookup_service = LookupService(config)
    lookup_teams, lookup_users = lookup_service.get_teams_and_users()

    rules = get_rules(lookup_users, lookup_teams)
    weights = get_weights()

    return rules, weights

generate()
