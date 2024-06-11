document.getElementById('sustainability-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const url = document.getElementById('url-input').value;
    const resultsSection = document.getElementById('results');
    const resultsContent = document.getElementById('results-content');
    
    resultsContent.innerHTML = `<p>Checking sustainability for: ${url}</p>`;
    
    // Simulate checking the sustainability
    setTimeout(() => {
        resultsContent.innerHTML = `
            <p>The brand appears to be <strong>eco-friendly</strong>.</p>
            <p>Here are some alternative sustainable products:</p>
            <ul>
                <li><a href="https://example.com/product1" target="_blank">Sustainable Product 1</a></li>
                <li><a href="https://example.com/product2" target="_blank">Sustainable Product 2</a></li>
                <li><a href="https://example.com/product3" target="_blank">Sustainable Product 3</a></li>
            </ul>
        `;
        resultsSection.classList.remove('hidden');
    }, 2000);
});
