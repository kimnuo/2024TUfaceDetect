document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('upload-face').addEventListener('click', function(event) {
        // 이미지 미리보기
        document.getElementById('inputimg').src = 'static/facedata/faceUp.jpg';

        // 서버로 요청 전송
        fetch('/upload-face', {
            method: 'POST'
        }).then(response => response.json())
          .then(data => console.log(data))
          .catch(error => console.error('Error:', error));
    });

    document.getElementById('capture-face').addEventListener('click', function() {
        const video = document.createElement('video');
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
                video.play();
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                setTimeout(() => {
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    const dataURL = canvas.toDataURL('image/jpeg');
                    document.getElementById('inputimg').src = dataURL;
                    stream.getTracks().forEach(track => track.stop());

                    // 이미지 데이터를 서버로 전송
                    fetch('/capture-face', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ image: dataURL })
                    })
                    .then(response => response.json())
                    .then(data => console.log(data))
                    .catch(error => console.error('Error:', error));
                }, 1000);
            })
            .catch(error => console.error('Error:', error));
    });

    document.getElementById('expBtn').addEventListener('click', function() {
        const imgSrc = document.getElementById('inputimg').src;
        fetch('/process', {
            method: 'POST',
            body: JSON.stringify({ image: imgSrc }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => response.json())
          .then(data => {
              document.getElementById('result').innerText = data.result;
          })
          .catch(error => console.error('Error:', error));
    });
});