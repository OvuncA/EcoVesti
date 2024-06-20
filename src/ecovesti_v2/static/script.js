document.getElementById('sustainability-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var urlInput = document.getElementById('url-input').value;
    document.getElementById('statusMessage').style.display = 'block';
    document.getElementById('statusText').innerText = 'Analyzing<span id="dots"></span>';
    document.getElementById('statusText').style.color = 'orange';

    // Create loading effect
    let dots = 0;
    const maxDots = 3;
    const loadingInterval = setInterval(() => {
        document.getElementById('dots').innerText = '.'.repeat(dots);
        dots = (dots + 1) % (maxDots + 1);
    }, 500);

    fetch('/analyze/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: urlInput }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Analysis Started:', data);

        const requestId = data.request_id;

        // Poll for result
        const pollInterval = setInterval(() => {
            fetch(`/result/${requestId}`)
                .then(response => response.json())
                .then(resultData => {
                    if (resultData.status === 'Processing') {
                        console.log('Still processing...');
                    } else {
                        clearInterval(pollInterval);
                        document.getElementById('result').innerText = resultData.result;
                        document.getElementById('results').classList.remove('hidden');
                        document.getElementById('statusMessage').style.display = 'none';
                        clearInterval(loadingInterval); // Stop the loading effect
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('statusText').innerText = 'An error occurred during the analysis.';
                    document.getElementById('statusText').style.color = 'red';
                    clearInterval(loadingInterval);
                    clearInterval(pollInterval);
                });
        }, 2000); // Poll every 2 seconds
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('statusText').innerText = 'An error occurred during the analysis.';
        document.getElementById('statusText').style.color = 'red';
        clearInterval(loadingInterval);
    });
});
