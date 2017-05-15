{
    "script": "for (item in myArray) { String id = item.get(\"id\")\nif (ctx._source.containsKey(id)) ctx._source.remove(id) }"
}
