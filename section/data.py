
  client.command("CREATE TABLE IF NOT EXISTS Data (\
  Consumption float, Date varchar(255), Read float, ConsumptionCost float, Cost float, TagId int, ValueType int, CostMeasurementUnitId float\
  ) ENGINE MergeTree")

  client.command("CREATE TABLE IF NOT EXISTS AggregatedData (\
  TagId int, Date varchar(255), Value float, ValueCurrency float, CurrencySymbol varchar(255), ValueType int\
  ) ENGINE MergeTree")

  client.command("CREATE TABLE IF NOT EXISTS InstantData (\
  UnitId int, Granularity varchar(255), TagId int, Date varchar(255), Average float, Minimum float, Maximum float, Last float, Count int, ValueType int\
  ) ENGINE MergeTree")
