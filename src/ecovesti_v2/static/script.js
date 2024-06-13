document.getElementById('sustainability-form').addEventListener('submit', function(e) {
    e.preventDefault();
    var urlInput = document.getElementById('url-input').value;
    document.getElementById('statusMessage').style.display = 'block';
    document.getElementById('statusText').innerText = 'Analyzing...';
    document.getElementById('statusText').style.color = 'orange';

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
        document.getElementById('statusText').innerText = 'Analysis Complete!';
        document.getElementById('statusText').style.color = 'green';

        var safeUrlName = 'final_product_report';
        var filename = safeUrlName + '_latest.txt';

        return fetch(`/static/${filename}`);
    })
    .then(response => {
        if (response.ok) {
            return response.text();
        } else {
            throw new Error('Analysis not complete or file not found.');
        }
    })
    .then(data => {
        document.getElementById('result').innerText = data;
        document.getElementById('results').classList.remove('hidden');
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('statusText').innerText = 'An error occurred during the analysis.';
        document.getElementById('statusText').style.color = 'red';
    });
});
