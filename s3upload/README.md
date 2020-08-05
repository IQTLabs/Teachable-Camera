# Container Creation

1. `sudo nano /etc/environment`

2. Add the following variables to the file:

    `ACCESS_KEY=<access key>`
    
    `SECRET_KEY=<secret key>`
    
3. Save the file and quit nano.

4. Then, log out of the Coral and log back in for the changes to take effect. 

5. Confirm that `ACCESS_KEY` and `SECRET_KEY` are in in the environment by typing `env`.

6. `cd /usr/local/eyeqt/containers`

7. `docker build -t eyeqt/upload:0.1 -t eyeqt/upload:latest .`

8. `docker run --detach --restart unless-stopped --name s3upload -e ACCESS_KEY=$ACCESS_KEY -e SECRET_KEY=$SECRET_KEY -v /home/mendel/capture:/capture -v /home/mendel/archive:/archive eyeqt/upload`


