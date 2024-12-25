# Documentation #



### Instructions on how to build/run the application ### 

<br>

##### 1. Install Python and create a virtual environment #####
a. **Install Python:** Ensure Python 3.x is installed on your machine. You can check the installed version by running ```python3 --version```.<br>
b. **Install pip:** Ensure pip (Python package installer) is installed.<br>

<br><br>

##### 2. Steps to build and run the application ##### 
a. **Extract the .bundle file**: First, place the shared `sudeendra_shenoy.bundle` file in any direcotry. Then in that directory execute the command `git init` to create a new Git repository. Next execute the command `git pull sudeendra_shenoy.bundle master` to pull files from the bundle file. <br>
b. **Set up a virtual environment**: Create and use virtual environment to manage dependencies: <br>
```
python3 -m venv venv
source venv/bin/activate
```
c. **Install Dependencies:** Install the required Python packages listed in the `requirements.txt` file:<br>
    ```pip install -r requirements.txt``` <br>

d. **Run the Application:** Run the application using the following commands:<br>
```
export FLASK_APP=payroll_application.py
export FLASK_ENV=development
flask run
```
<br><br>

##### 3. Using the application ##### 



a. **Upload CSV file**: Use Postman to upload a CSV file
* Open Postman and create a new POST request.
* Set the URL to http://127.0.0.1:5000/upload-file
* In the `body` tab, select `form-data` and add a key named file of type file.
* Select your CSV file to upload.
* Click `Send` and check the response.

<br>

b. **Retrieve the data from database:** Use Postman to retrieve the uploaded data
* Create a new GET request.
* Set the URL to: http://127.0.0.1:5000/get-data
* Click `Send` and check the response.

<br>

c. **Retrieve the Payroll Report:** Use Postman to retrieve the payroll report
* Create a new GET request.
* Set the URL to http://127.0.0.1:5000/get-payroll-report
* Click `Send` and check the response.



___

<br>


###  How did you test that your implementation was correct?
Testing was performed using the following approach: <br>

**Using Postman:** <br>
* **Upload Endpoint** (http://127.0.0.1:5000/upload-file):
  * **Valid file upload:**  Upload a valid CSV file and ensure the API returns a success message ("File successfully uploaded and saved"). <br>
  * **Invalid file format upload:**  Try uploading a non-CSV file and check for an appropriate error message.
  * **Duplicate File:**  Upload the same csv file twice and verify that the second upload returns "File already exists" message. <br><br>

* **Data Retrieval Endpoint** (http://127.0.0.1:5000/get-data):
  * **Check Data:** Verify that all uploaded data is correctly returned by the API. <br><br>

* **Generate Report Endpoint** (http://127.0.0.1:5000/get-payroll-report):
  * **Correct Calculation:** Upload a CSV file with known values and manually verify that the payroll report calculations are correct. Check multiple pay periods and different job groups. <br><br>

___

<br>

#### 2. If this application was destined for a production environment, what would you add or change?
When preparing a Flask application for a production environment few of the additions or changes that we can make are: <br>
   a). **Use a Production-Ready Web Server:** <br>
       - Instead of the built-in Flask server, we must use a production-ready server like Gunicorn.
   
   b). **Database Configurations:** <br>
       - We can use a robust database like PostgreSQL or MySQL instead of SQLite as these databases are designed for scalability and can handle larger datasets and complex queries more efficiently than SQLite.
   
   c). **Environment Variables:** <br>
       - Store sensitive configurations such as database URIs, secret keys, and other credentials in environment variables or a vault such as HashiCorp or  Akeyless.

   d). **Error Handling:** <br>
       - Implement robust error handling to manage unexpected errors and return appropriate responses.

   e). **Logging:** <br>
       - Configure logging to keep track of application behavior and errors with distinct levels of logging.

   f). **Documentation:** <br>
       - Provide comprehensive documentation for your API endpoints, including example requests and responses. Use tools like Swagger or Postman for API documentation.<br><br>

___

<br>

### What compromises did you have to make as a result of the time constraints of this challenge?
Given the time constraints of this challenge, few of the areas where compromises have been made are:<br>

a. **Simplified Error Handling:** <br>
&emsp; &emsp; - In reality, error handling would be more comprehensive by using custom error handlers for different types of errors.

b. **Basic Input Validation:** <br>
&emsp; &emsp; - A thorough validation that includes checking the file content format, structure, ensuring data is present and not just the file extension.

c. **Minimal Tests:** <br>
&emsp; &emsp; - Extensive testing that includes edge cases, invalid inputs, and end-to-end tests using some frameworks.

d. **Basic Database Configuration:** <br>
&emsp; &emsp; - For production, a robust database system like PostgreSQL or MySQL would be used.
