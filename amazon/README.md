## Amazon Scrapper

This script scraps data from amazon 

- Insert keyword, for example "lenovo legion 5"
![image](https://user-images.githubusercontent.com/57668465/176938010-cba6a574-4ba4-445e-9c53-c15877353ff2.png)

- Script will get the data for:
    - Product name
    - Image's link
    - Product rating
    - Number of rating
    - Product price 
    - USD (hard code)
 
![image](https://user-images.githubusercontent.com/57668465/176938587-5da48d3c-c41e-4361-a6a0-5165bdcac2b3.png)

`example result`
| product_name  |  product_image | product_rating | no_of_review | min_price | max_price | price | currency |
| ------------- | ------------- |------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 2022 Lenovo Legion Gaming Laptop ...| https://m.media-amazon.com/images/I/71jx6w2AscL._AC_UY218_.jpg | 4 | 5 | 989.99 | 989.99 | 989.99 | USD |
| Lenovo Legion 5 Gaming Laptop, 15.6" FHD ... | https://m.media-amazon.com/images/I/61ZWPLVZLHL._AC_UY218_.jpg | 4.6 | 2143 | 1295 | 1295 | 1295 | USD |
  
Note: 
- You have to add additional web driver that match with your driver
- If there are changes in the web page, you have to update the logic
