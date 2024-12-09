
import React from 'react';
import { Pagination } from '@material-ui/lab';

function DataTablePagination({ page, count, onChange }) {
  return (
    <Pagination
      page={page}
      count={count}
      onChange={(event, value) => onChange(value)}
      variant="outlined"
      shape="rounded"
    />
  );
}

export default DataTablePagination;
