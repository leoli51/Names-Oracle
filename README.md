# Names-Oracle

The `names_oracle` module is an easy solution to analyze names and last names.
It provides information about countries, sex, for first and last names.
See examples below to see all the extracted information.

This project was inspired and based on the [names-dataset](https://github.com/philipperemy/name-dataset) project by Philippe Remy.

## Install

To install:

```bash
pip install names-oracle
```

Note: the package contains the database of names, so it is quite heavy ~2Gb.

## How to use

Import:

```bash
>>> import names_oracle
```

The module is composed of just a couple of functions. The most important being:

`get_name_info(name : str, country : str) -> Union[Dict[str: float], None]`

This function retrieves the data(if present) for the given name for a given country. The list of
available countries can be retrieved through the `get_available_countries() -> list[str]` function.
The available countries are:

```bash
>>> import names_oracle
>>> names_oracle.get_available_countries()
['AE', 'AF', 'AL', 'ALL', 'AO', 'AR', 'AT', 'AZ', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BN', 'BO', 'BR', 'BW', 'CA', 'CH', 'CL', 'CM', 'CN', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DZ', 'EC', 'EE', 'EG', 'ES', 'ET', 'FI', 'FJ', 'FR', 'GB', 'GE', 'GH', 'GR', 'GT', 'HK', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IN', 'IQ', 'IR', 'IS', 'IT', 'JM', 'JO', 'JP', 'KH', 'KR', 'KW', 'KZ', 'LB', 'LT', 'LU', 'LY', 'MA', 'MD', 'MO', 'MT', 'MU', 'MV', 'MX', 'MY', 'NA', 'NG', 'NL', 'NO', 'OM', 'PA', 'PE', 'PH', 'PL', 'PR', 'PS', 'PT', 'QA', 'RS', 'RU', 'SA', 'SD', 'SE', 'SG', 'SI', 'SV', 'SY', 'TM', 'TN', 'TR', 'TW', 'US', 'UY', 'YE', 'ZA']
```

If you want to retrieve the data for all countries merged you can use `"ALL"` as country code.

**Note: The first time you retrieve information for a country its database is loaded in memory, this is why the first call is always slow.**

**Note: The ALL database is the biggest one (~1Gb) as it contains all other databases merged together, therefore it takes some time to load.**

```bash
>>> from pprint import pprint
>>> import names_oracle
>>> name_data = names_oracle.get_name_info("Andrea", "IT")
>>> pprint(name_data)
{'female_frequency': 11707,
 'female_probability': 0.026372522296236392,
 'first_name_frequency': 443909,
 'first_name_norm_frequency': 0.916561364387182,
 'first_name_probability': 0.9750327274005218,
 'last_name_frequency': 11367,
 'last_name_norm_frequency': 0.08547773382863846,
 'last_name_probability': 0.02496727259947812,
 'male_frequency': 432202,
 'male_probability': 0.9736274777037636,
 'name': 'Andrea'}
>>> name_data = names_oracle.get_name_info("Andrea", "DE")
>>> pprint(name_data)
{'female_frequency': 23848,
 'female_probability': 0.9767765717796436,
 'first_name_frequency': 24415,
 'first_name_norm_frequency': 0.3445964065433092,
 'first_name_probability': 0.9890221177995625,
 'last_name_frequency': 271,
 'last_name_norm_frequency': 0.0062432326583269976,
 'last_name_probability': 0.010977882200437494,
 'male_frequency': 567,
 'male_probability': 0.023223428220356338,
 'name': 'Andrea'}
```

To determine which part of a name is the first name and which part is the last name you can use the following function:

`split_name_in_first_and_last(name, country) -> list`

This function returns a string with te first and last name or an empty list if it couldn't determine them.

```bash
>>> import names_oracle
>>> name_parts = names_oracle.split_name_in_first_and_last("Leonardo La Rocca", "IT")
>>> print(name_parts)
['Leonardo', 'La Rocca']
>>> name_parts = names_oracle.split_name_in_first_and_last("La Rocca Leonardo", "IT")
>>> print(name_data)
['Leonardo', 'La Rocca']
```

## Sources

The database was generated from the [Facebook massive dump (533M users)](https://www.theguardian.com/technology/2021/apr/03/500-million-facebook-users-website-hackers).

You can download the original dataset [here](https://drive.google.com/file/d/1wRQfw5EYpzulvRfHCGIUWB2am5JUYVGk/view).