class BodyProcessedResults:
    def __init__(self, table_or_view_name_to_columns_dic=None, constraints=None):
        if not table_or_view_name_to_columns_dic:
            self.table_or_view_name_to_columns_dic = {}
        else:
            self.table_or_view_name_to_columns_dic = table_or_view_name_to_columns_dic
        if not constraints:
            self.constraints = []
        else:
            self.constraints = constraints
