# shed-of-graphs

## How to host server
### Windows
1. **Install and configure wsl**
2. **Follow the steps for hosting on Ubuntu**

### Ubuntu
1. **Install docker cli**
2. **Download the project to your machine**
3. **Create the '/host/backup/hist/img' directory**
    ```bash
    sudo mkdir -p /host/backup/hist/img
    ```
4. **Run the following commands in the the project directory with the port where you want the webinterface to be accessible**
    ```bash
    sudo docker build --target prod -t shed-of-graphs:prod .
    sudo docker run -p {port}:5000 -v /host/backup:/backup shed-of-graphs:prod
    ```
5. **The server is now accessible at http://localhost:{port} on your machine**

**OR**

1. **Install python**
2. **Download the project to your machine**
3. **Open a terminal in the src/app/plantri54 directory inside the project and run the following command**
    ```bash
    make
    ```
3. **Add the plantri file you created to your path**
    ```bash
    sudo nano ~/.bashrc # add the following to the end of the file: export PATH=$PATH:/path/to/the/plantri/file
    source ~/.bashrc # applies the changes
    ```  
4. **Run the host-linux.sh file located in the root directory of the project**
5. **You can access the webinterface via the link provided in the console**


## Common Issues
- If the web interface doesn't work, try using Google Chrome as your browser.
- If some scripts dont run on linux you might have to change the line endings from CRLF to LF
    ```bash
    dos2unix <file>
    ```


## How to setup dev environment
1. **Install python**
2. **Install github cli**
3. **Authenticate using github cli**
    ```bash
    gh auth login
    ```
4. **Clone the repository to your machine**
    ```bash
    gh repo clone Mirovh/shed-of-graphs
    ```
5. **Execute the setup dev file for your OS**
6. **Open the shed-of-graphs root folder with vs code**
7. **When modifying requirements-dev.txt, rerun the setup dev file to rebuild the dev virtual environment. This updates the packages accessible to the vs code IDE automatically too**
