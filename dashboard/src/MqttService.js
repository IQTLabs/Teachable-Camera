import mqtt from "mqtt";

const host = window.location.hostname;
console.log("window.location.hostname: " + host);
const url = new URL(window.location.href);
console.log("url: " + url);
url.protocol = "ws:";
url.port = 9001;
url.pathname = "/";
console.log("url: " + url);
const websocketUrl = url.toString(); //"ws://192.168.1.200:9001";
const apiEndpoint = "/eyeqt";
function getClient() {
  const client = mqtt.connect(websocketUrl);
  client.stream.on("error", (err) => {
    //errorHandler(`Connection to ${websocketUrl} failed`);
    client.end();
  });
  return client;
}
function subscribe(client, topic) {
  const callBack = (err, granted) => {
    if (err) {
      console.log("Subscription request failed");
    }
  };
  return client.subscribe(apiEndpoint + topic, callBack);
}
function onMessage(client, callBack) {
  client.on("message", (topic, message, packet) => {
    callBack(message, topic);
  });
}
function unsubscribe(client, topic) {
  client.unsubscribe(apiEndpoint + topic);
}
function closeConnection(client) {
  client.end();
}
const mqttService = {
  getClient,
  subscribe,
  onMessage,
  unsubscribe,
  closeConnection,
};
export default mqttService;