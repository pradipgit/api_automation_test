import pandas as pd


class ExcelClient:

    def __init__(self):
        pass

    def multiple_dfs(self, df_list, sheets, file_name, spaces):
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        row = 0
        for dataframe in df_list:
            dataframe.to_excel(writer, sheet_name=sheets, startrow=row, startcol=0)
            row = row + len(dataframe.index) + spaces + 1
        writer.save()

    def merge_dfs(self, records):
        records_set = pd.concat(records)

        return records_set

    def write_to_excel(self, records, output_file_name):

        writer = pd.ExcelWriter(output_file_name, engine='xlsxwriter')

        workbook = writer.book
        # excel sheet formatting
        format1 = workbook.add_format({'num_format': '#,##0',  'align': 'center'})
        format2 = workbook.add_format({'align': 'left'})
        row = 0

        for record in records:
            record['data'].to_excel(writer, sheet_name=record['sheet_name'], startrow=row, startcol=0)
            worksheet = writer.sheets[record['sheet_name']]
            worksheet.set_column('A:A', 42, format2)
            worksheet.set_column('B:B', 10, format1)
            worksheet.set_column('F:F', 10)

        writer.save()
