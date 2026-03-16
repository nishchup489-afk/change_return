cost = float(input("Enter the cost : (in dollars) "))
given = float(input("Enter the given amount : (in dollars) "))


def change_return(cost , given ):
    cost *= 100
    given *= 100


    if given < cost :
        pending = cost - given
        return ({
            "status" : "pending" , 
            "amount" : pending / 100
        
        })

    coins = [
        ("100$", 10000),
        ("50$", 5000),
        ("20$", 2000),
        ("10$", 1000),
        ("5$", 500),
        ("1$", 100),
        ("quarter", 25),
        ("dime", 10),
        ("nickel", 5),
        ("cent", 1)
    ]
    
    
    change = given - cost

    result = {}

    for name , value in coins :
        count = change // value

        if count > 0:
            result[name] = count
            change -= count * value
    return {
        "status" : "success",
        "change" : result
    
    }


print(change_return(cost , given))