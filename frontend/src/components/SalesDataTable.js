import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
  TableContainer,
} from '@material-ui/core';
import Pagination from './Pagination';

function SalesDataTable({ data }) {
  return (
    <TableContainer component={Paper}>
      <Table aria-label="sales data table">
        <TableHead>
          <TableRow>
            <TableCell>Order ID</TableCell>
            <TableCell>Customer Name</TableCell>
            <TableCell>Total Amount</TableCell>
            <TableCell>Order Date</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.orders.map((order) => (
            <TableRow key={order.id}>
              <TableCell>{order.id}</TableCell>
              <TableCell>{order.customer_name}</TableCell>
              <TableCell>{order.total}</TableCell>
              <TableCell>{order.created_at}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Pagination
        page={data.current_page}
        count={data.total_pages}
        onChange={data.onPageChange}
      />
    </TableContainer>
  );
}

export default SalesDataTable;
