## Input examples:
### POST http://127.0.0.1:5000/user/login
```JSON
  {
    "authorization": {
      "name": "Morty",
      "password": "229"
    }
  }
```

### POST http://127.0.0.1:5000/user/new
```JSON
  {
    "authorization": {
      "name": "Morty",
      "password": "229",
      "confirm_password": "229"
    }
  }
```

### POST http://127.0.0.1:5000/post/new
```JSON
  {
    "post": {
      "slug": "i-am-in-space",
      "creator": "Morty",
      "title": "Get me out of here, RICK!1"
    }
  }
```

### GET http://127.0.0.1:5000/post/get/super-slug
#### RETURN:
```JSON
  {
      "_id": {
          "$oid": "5b151bef36f0572f7ce98bac"
      },
      "comments": [
          {
              "$oid": "5b152b4136f05734047f697b"
          }
      ],
      "created_at": {
          "$date": 1528110063472
      },
      "creator": "Pony",
      "rates": [],
      "slug": "super-slug",
      "title": "will buy some apples"
  }
```


### POST http://127.0.0.1:5000/post/rate
```JSON
  {
    "post": {
      "post_id": "5b153d2236f0572e345d63f3",
      "user_id": "5b1508db36f0572bd859f291",
      "rate": 5
    }
  }
```

### GET http://127.0.0.1:5000/post/rate/get/5b153d2236f0572e345d63f3
#### RETURN:
```JSON
  {
      "rates": [
          {
              "rate": 5,
              "user_id": "5b1508db36f0572bd859f291"
          }
      ]
  }
```

### PUT http://127.0.0.1:5000/comment/new
```JSON
  {
    "comment": {
      "post_id": "5b15476c36f0571774febfa9",
      "creator": "Morty",
      "text": "GET ME HOME, YOU OLD LUNATIC"
    }
  }
```

### GET http://127.0.0.1:5000/comment/get/5b15517636f05727b888684a
#### RETURN:
```JSON
  {
      "_id": {
          "$oid": "5b15517636f05727b888684a"
      },
      "creator": "Morty",
      "text": "GET ME HOME, YOU OLD LUNATIC"
  }
```



