document.addEventListener('DOMContentLoaded', function () {
    const countryField = document.querySelector('#id_country');
    const universityField = document.querySelector('#id_university');
    const countryEducationField = document.querySelector('#id_doctor_education-0-country');
    const universityEducationField = document.querySelector('#id_doctor_education-0-university');


    countryField.addEventListener('change', function () {
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
                    option.id = uni.country;
                    universityField.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching universities:', error));
    });


    countryEducationField.addEventListener('change', function () {
        const selectedCountry = countryEducationField.value;
        fetch(`https://raw.githubusercontent.com/Hipo/university-domains-list/refs/heads/master/world_universities_and_domains.json`)
            .then(response => response.json())
            .then(data => {
                const filteredUniversities = data.filter(uni => uni.countryEducationField === selectedCountry);
                universityEducationField.innerHTML = '';

                filteredUniversities.forEach(uni => {
                    const option = document.createElement('option');
                    option.value = uni.name;
                    option.textContent = uni.name;
                    option.id = uni.country;
                    universityEducationField.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching universities:', error));
    });
});



