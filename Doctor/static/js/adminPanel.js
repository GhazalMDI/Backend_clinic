alert('hi')
document.addEventListener('DOMContentLoaded', function() {
    const countryField = document.querySelector('#id_country');
    const universityField = document.querySelector('#id_university');

    countryField.addEventListener('change', function() {
        const selectedCountry = countryField.value;
        fetch(`https://raw.githubusercontent.com/Hipo/university-domains-list/refs/heads/master/world_universities_and_domains.json`)
            .then(response => response.json())
            .then(data => {
                const filteredUniversities = data.filter(uni => uni.country === selectedCountry);

                universityField.innerHTML = '';

                filteredUniversities.forEach(uni => {
                    const option = document.createElement('option');
                    option.value = uni.name;
                    option.textContent = uni.name;
                    universityField.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching universities:', error));
    });
});
