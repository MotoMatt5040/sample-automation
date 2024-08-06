from ml.machine_learning import stratified_split

class Tarrance:

    def __init__(self, data):
        self.data = data
        self._headers = data.columns.to_list()
        self.data.VTYPE = self.data.cell.apply(lambda x: 1 if x == 'N' else 2)
        self.data.MD = self.data.cell.apply(lambda x: 1 if x == 'Y' else '')
        print(self.data.head().to_string())
        batches = stratified_split(self.data, ['region', 'fourage', 'Sex'])
        print()
        for i, batch in enumerate(batches):
            print(
                '-'*50+'\n',
                f"Batch {i + 1}:\n",
                # batch,
                f"\nLength: {len(batch)}",
                f'\nRegion Counts: {batch['region'].value_counts()}',
                f'\nFourage Counts: {batch['fourage'].value_counts()}',
                f'\nSex Counts: {batch['Sex'].value_counts()}')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers=None):
        self._headers = headers



