# Teachable Camera Dashboard

This is a web based dashboard for Teachable Camera. It lets you see what objects have been detected and provides a live view of the camera feed. It is intended to be a starting point for building out a more complete application.

[Dashboard screenshot](../images/dashboard.png)

## Design
The web app is built using React with the Martial UI framework. It was started off of the Martial UI Dashboard example. The video feed is simply a JPEG image that gets progressively updated. A Javascript MQTT client is used to receive object detection information.

The web app gets compiled into a set of static files that are served up by the Coral Board. The [dashboard-server](../dashboard-server/README.md) container handles serving these files. The static files must be compiled on a separate computer because there is not enough memory on the Coral board to do it there. 

If you make changes to the web app, you need to recompile the static files, copy them to the dashboard-serve folder and then move the updated `dashboard-serve` folder to the Coral board using `scp`.

## Making updates to the Dashboard
*Follow these steps if you would like to make changes to the Dashboard Web App. If you are happy with it, then you can skip all this.*

### Install Tools

1. On a separate computer install Node (which comes with NPM). 

2. In this directory run `npm install`

### Compile Static Files and Publish

1. In this directory run 'npm run build`. This will compile an updated set of static files in the **build** sub-directory.

2. Run the `./move_to_prod.sh` script which will copy the files in **build** to the **dashboard-serve/build** folder.

3. Move the **dashboard-serve** folder over to the Coral Board using `scp`. It should overwrite the **dashboard-serve** folder in the repo on the Coral Board. For example:
````
// Modify for your system!! JUST AN EXAMPLE
% scp -r dashboard-serve mendel@192.168.1.200:~/teachable-camera-software/
````

4. On the Coral Board, in the teachable-camera repo, run `docker-compose build` to build a new version of the dashboard container with the updated web app.

5. 🎉 Celebrate 👏🏾
