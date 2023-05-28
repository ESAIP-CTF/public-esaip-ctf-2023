# Mario visits the human kingdom 1

## Description
```
Luigi has decided to leave the Mushroom Kingdom to devote himself to his true passion: technician.
He sent this picture to his brother Mario and challenged him to find his new workplace.
Mario is not very good in OSINT and asked you to help him to find the coordinates of his brother's workplace so that he could visit him.
```

## Flag
**`ECTF{47.229889:-1.497611}`**

## Resolution
- Find the city from the right sign => SECURITESS => Nantes
- Find the company where Luigi works => train deduction (on the left on the image) => SNCF
- Find the coordinates of the place of work => train technician => list of maintenance sites (technicentres) => https://ressources.data.sncf.com/explore/dataset/sites-de-livraison-sncf-ti-geoparts-v2/ => Nantes => 47.229889, -1.497611