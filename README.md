# 📊 DataMatrix Transformer 🛠️

Welcome to the DataMatrix Transformer repository! This project is designed to simplify and enhance the resizing of data matric qr codes using Python (using libdmtx and treepoem) 🐍 and Docker 🐳.
Features ✨

- Efficient Data Processing: Transform data matric codes with ease
- Scalable: Utilize Docker to ensure scalability and consistency
- Easy to Use: Ready to run Docker containers are provided
- Provides an easy to use open API
 
Getting Started 🚀
---
Clone the Repository:

`git clone https://github.com/deep2web/DataMatrix-Transformer.git`

Navigate to the Project Directory:

`cd DataMatrix-Transformer`

Build the Docker Image:

`docker buildx build -t datamatrix-transformer .`

Run the Docker Container:

`docker run -p 80:8000 datamatrix-transformer`

Alternatively there is also a prebuild Docker image provided:

`docker pull ghcr.io/deep2web/datamatrix-transformer:main`

Access API docs via `localhost:80/docs`

Contributing 🤝
---
I welcome contributions! Feel welcome to open a Pull request or Issue.

License 📜
---
This project is licensed under the GNU General Public License - see the LICENSE file for details.
