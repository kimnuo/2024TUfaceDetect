"use strict";

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('upload-face').addEventListener('click', function (event) {
    // 이미지 미리보기
    document.getElementById('inputimg').src = 'static/facedata/faceUp.jpg'; // 서버로 요청 전송

    fetch('/upload-face', {
      method: 'POST'
    }).then(function (response) {
      return response.json();
    }).then(function (data) {
      return console.log(data);
    })["catch"](function (error) {
      return console.error('Error:', error);
    });
  });
  document.getElementById('capture-face').addEventListener('click', function () {
    var video = document.createElement('video');
    navigator.mediaDevices.getUserMedia({
      video: true
    }).then(function (stream) {
      video.srcObject = stream;
      video.play();
      var canvas = document.createElement('canvas');
      var context = canvas.getContext('2d');
      setTimeout(function () {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        var dataURL = canvas.toDataURL('image/jpeg');
        document.getElementById('inputimg').src = dataURL;
        stream.getTracks().forEach(function (track) {
          return track.stop();
        }); // 이미지 데이터를 서버로 전송

        fetch('/capture-face', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            image: dataURL
          })
        }).then(function (response) {
          return response.json();
        }).then(function (data) {
          return console.log(data);
        })["catch"](function (error) {
          return console.error('Error:', error);
        });
      }, 1000);
    })["catch"](function (error) {
      return console.error('Error:', error);
    });
  });
  document.getElementById('expBtn').addEventListener('click', function () {
    var imgSrc = document.getElementById('inputimg').src;
    fetch('/process', {
      method: 'POST',
      body: JSON.stringify({
        image: imgSrc
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(function (response) {
      return response.json();
    }).then(function (data) {
      document.getElementById('result').innerText = data.result;
    })["catch"](function (error) {
      return console.error('Error:', error);
    });
  });
});