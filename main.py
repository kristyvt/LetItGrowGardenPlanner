# Import data connection to start program
import data_connection

# Test that database exists and can connect before launching

test_connection = data_connection.Connection()
if test_connection.status == "success":
    import window
    import plant
    import plant_set
elif test_connection.status == "failed":
    print("Database does not exist, please install Garden database and try again")
else:
    print("other error")


exit(0)
