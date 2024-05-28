few_shots=[
    {
        'Question':'how many nike white color xs tshirt do i have',
        'SQLQuery':"SELECT stock_quantity FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
        'SQLResult':'Result of SQL Query',
        "Answer":"32"
    },

    {
        'Question':'how much is the inventory for all small size tshirts',
        'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
        'SQLResult':'Result of SQL Query',
        "Answer":"15731"
    },
    {
        'Question':'if i sell all the nike shirts today with discount applied how much money will i get',
        'SQLQuery':"select sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) from(select t_shirt_id ,price*stock_quantity as total_amount from t_shirts where brand = 'Levi') a left join discounts on a.t_shirt_id = discounts.t_shirt_id",
        'SQLResult':'Result of SQL Query',
        "Answer":"15535.400000"
    },
    {

        'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
        'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
        'SQLResult': "Result of the SQL query",
        'Answer' : "15866"
    },
    {
        'Question': "How many white color Levi's shirt I have?",
        'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
        'SQLResult': "Result of the SQL query",
        'Answer' : "38"


    }

]
