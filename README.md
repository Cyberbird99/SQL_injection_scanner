This is a basic example of a SQL Injection scanner. It only looks for common SQL error messages, which is a limited approach.
Scans a webpage for HTML form elements.

This script:  
Tests these forms by injecting common SQL injection characters (" and ') into the form fields.  
Sends the form data back to the server, either via POST or GET requests.  
Checks the server response for common SQL error messages, which could indicate that the site is vulnerable to SQL injection.  
Reports whether the target URL is vulnerable to SQL injection based on the error messages returned by the server.


Ethical Considerations: Always have permission before running any kind of security scan on websites that you don't own or have explicit consent to test. Unauthorized testing of websites may be illegal.
