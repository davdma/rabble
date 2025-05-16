* Rubric item: author and subRabble fields display a numeric key instead of a username/identifier
    * I addressed the rubric item by adding SlugRelatedField to the post serializer,
    now you can make POST requests using the username and subrabble name, and the fields
    do not display integers but strings now.
    * Changes were made to `api/serializers.py` and `api/views.py`
* Rubric item: clicking on the thumbs-up icon does not update the number of likes
    * I addressed the rubric item by adding a likes endpoint to my api
    along with a post_like view function. I also added frontend changes to enable
    sending the POST request for updating likes.
    * Changes were made to `api/urls.py`, `api/views.py`, and `post_detail.html`.