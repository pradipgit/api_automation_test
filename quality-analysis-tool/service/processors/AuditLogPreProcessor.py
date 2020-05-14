import service.constant as constant


class AuditLogPreProcessor():

    def __init__(self):
        pass

    # Prepares Audit-logs for processing, filters properties
    def pre_process_audit_logs(self, config, auditlogs, fixed_size_dataset):

        user_attributes = config['USER_ATTRIBUTES'].encode('ascii')
        user_attr_list = user_attributes.split(',')

        team_attributes = config['TEAM_ATTRIBUTES'].encode('ascii')
        team_attr_list = team_attributes.split(',')

        component_attributes = config['COMPONENT_ATTRIBUTES'].encode('ascii')
        component_attr_list = component_attributes.split(',')

        sub_component_attributes = config['SUB_COMPONENT_ATTRIBUTES'].encode('ascii')
        sub_component_attr_list = sub_component_attributes.split(',')

        action_attributes = config['ACTION_ATTRIBUTES'].encode('ascii')
        action_attr_list = action_attributes.split(',')

        processed_logs = []

        if fixed_size_dataset:
            for log in auditlogs:
                logs = self.parse_attributes(log, user_attr_list, team_attr_list, component_attr_list, sub_component_attr_list, action_attr_list, True)
                processed_logs.append(logs)
        else:
            for log in auditlogs:
                logs = self.parse_attributes(log, user_attr_list, team_attr_list, component_attr_list, sub_component_attr_list, action_attr_list, False)
                processed_logs.append(logs)

        return processed_logs

    # Parses the audit-log payload for possible attributes
    def parse_attributes(self, log, user_attr_list, team_attr_list, component_attr_list, subcomponent_attr_list, action_attr_list, include_default):

        log = self.parse_user_attribute(log, user_attr_list, include_default)
        log = self.parse_team_attribute(log, team_attr_list, include_default)
        log = self.parse_component_attribute(log, component_attr_list, include_default)
        log = self.parse_sub_component_attribute(log, subcomponent_attr_list, include_default)
        log = self.parse_action_attribute(log, action_attr_list)

        return log

    def parse_user_attribute(self, log, user_list, include_default=False):

        for attr in user_list:
            if log.has_key(str(attr)):
                log.update({constant.USER_ATTRIBUTE: log[attr]})

            elif log.has_key('tags') and log["tags"].has_key(attr):
                log.update({constant.USER_ATTRIBUTE: log["tags"][attr]})

            elif log.has_key('messageContent') and log['messageContent'].has_key(attr):
                log.update({constant.USER_ATTRIBUTE: log["messageContent"][attr]})

            elif log.has_key('messageContent') and log["messageContent"].has_key('tags') and log['messageContent']['tags'].has_key(attr):
                log.update({constant.USER_ATTRIBUTE: log["messageContent"]['tags'][attr]})

            elif include_default:
                log.update({constant.USER_ATTRIBUTE: 'NAN'})

        return log

    def parse_team_attribute(self, log, team_list, include_default=False):

        for attr in team_list:
            if log.has_key(str(attr)):
                log.update({constant.TEAM_ATTRIBUTE: log[attr]})

            elif log.has_key('tags') and log["tags"].has_key(attr):
                log.update({constant.TEAM_ATTRIBUTE: log["tags"][attr]})

            elif log.has_key('messageContent') and log['messageContent'].has_key(attr):
                log.update({constant.TEAM_ATTRIBUTE: log["messageContent"][attr]})

            elif log.has_key('messageContent') and log["messageContent"].has_key('tags') and log['messageContent'][
                'tags'].has_key(attr):
                log.update({constant.TEAM_ATTRIBUTE: log["messageContent"]['tags'][attr]})
            elif include_default:
                log.update({constant.TEAM_ATTRIBUTE: 'NAN'})

        return log

    def parse_component_attribute(self, log, component_list, include_default=False):

        for attr in component_list:

            if log.has_key('tags') and log["tags"].has_key(attr):
                val = log['tags'][attr]
                log.update({constant.COMPONENT_ATTRIBUTE: val})

            elif log.has_key('messageContent') and log['messageContent'].has_key(attr):
                val = log["messageContent"][attr]
                log.update({constant.COMPONENT_ATTRIBUTE: val})

            elif log.has_key('messageContent') and log["messageContent"].has_key('tags') and log['messageContent'][
                'tags'].has_key(attr):
                log.update({constant.COMPONENT_ATTRIBUTE: log["messageContent"]['tags'][attr]})

            elif log.has_key(str(attr)):
                val = log[attr]
                log.update({constant.COMPONENT_ATTRIBUTE: val})
            elif include_default:
                log.update({constant.COMPONENT_ATTRIBUTE: 'NAN'})

        return log

    def parse_sub_component_attribute(self, log, sub_component_list, include_default=False):

        for attr in sub_component_list:
            if log.has_key(str(attr)):
                log.update({constant.SUB_COMPONENT_ATTRIBUTE: log[attr]})

            elif log.has_key('tags') and log["tags"].has_key(attr):
                log.update({constant.SUB_COMPONENT_ATTRIBUTE: log["tags"][attr]})

            elif log.has_key('messageContent') and log['messageContent'].has_key(attr):
                log.update({constant.SUB_COMPONENT_ATTRIBUTE: log["messageContent"][attr]})

            elif log.has_key('messageContent') and log["messageContent"].has_key('tags') and log['messageContent'][
                'tags'].has_key(attr):
                log.update({constant.SUB_COMPONENT_ATTRIBUTE: log["messageContent"]['tags'][attr]})
            elif include_default:
                log.update({constant.SUB_COMPONENT_ATTRIBUTE: 'NAN'})

        return log

    def parse_action_attribute(self,log, action_list):

        for attr in action_list:
            if log.has_key(str(attr)):
                log.update({constant.ACTION_ATTRIBUTE: log[attr]})

            elif log.has_key('tags') and log["tags"].has_key(attr):
                log.update({constant.ACTION_ATTRIBUTE: log["tags"][attr]})

            elif log.has_key('messageContent') and log['messageContent'].has_key(attr):
                log.update({constant.ACTION_ATTRIBUTE: log["messageContent"][attr]})

            elif log.has_key('messageContent') and log["messageContent"].has_key('tags') and log['messageContent'][
                'tags'].has_key(attr):
                log.update({constant.ACTION_ATTRIBUTE: log["messageContent"]['tags'][attr]})
            else:
                log.update({constant.ACTION_ATTRIBUTE: 'NAN'})

        return log
