from example import WorkingHourManager, initialize_database

def main():
    initialize_database(WorkingHourManager.DB_PATH)
    whm = WorkingHourManager()
    # whm.log(1, 3600, '2019-01-01')

    hours = whm.total(1, '2019-01-01', '2019-01-31')
    
    print(hours)

    salary = whm.salary(1, '2019-01-01', '2019-01-31')
    print(salary)


if __name__ == '__main__':
    main()
