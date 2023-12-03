function makeBridgeTable(
  tableName: string,
  column1Name: string,
  column1Range: number,
  column2Name: string,
  column2Range: number,
  numRows: number
) {
  let query = "";
  let num = 0;
  for (let i = 1; i < column1Range; i++) {
    for (let j = 1; j < column2Range; j++) {
      query += `insert into ${tableName} (${column1Name}, ${column2Name}) values (${i}, ${j});\n`;
      num += 1;
      if (num === numRows) {
        return query;
      }
    }
  }
  return query;
}

const query = makeBridgeTable(
  "employee_billing",
  "statement_id",
  50,
  "employee_id",
  50,
  200
);

console.log(query);
