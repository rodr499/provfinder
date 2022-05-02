function getRegions(type) {

    let selectOptions;

    selectOptions = refreshSelect('city')

    if (type == 'state') {
        id = document.getElementById('country_code').value;
        
    } else if (type == 'city') {
        id = document.getElementById('state').value;
        
    }
    
    selectOptions = refreshSelect(type)

    url = `/regions/${type}/${id}`;

    fetch(url)
        .then(
            function(response) {
                if (response.status !== 200) {
                    console.warn('Look like there was a problem. Status Code: ' + response.status);
                    return;
                }
                response.json().then(function(data) {
                 let option;
                    for (var i in data) {
                        option = document.createElement('option');
                        option.text = data[i];
                        option.value = i;
                        selectOptions.add(option)
                    }
                })
            }
        )
        .catch(function(err) {
            console.error('Fatch Error - ', err)
        });
}

function refreshSelect(type) {
    selectOptions = document.getElementById(type);
    selectOptions.length = 0;
    let defaultOption = document.createElement('option');
    defaultOption.text = `Select ${type}`;
    defaultOption.disabled = true;

    selectOptions.add(defaultOption);
    selectOptions.selectedIndex = 0;
    return selectOptions
}