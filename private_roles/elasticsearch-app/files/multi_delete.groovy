{
    "script": "for (item in myArray) { String id = item.get(\"id\")\nString value = item.get(\"value\")\nif (ctx._source.containsKey(id)) { if (ctx._source[id].contains(value) == true) ctx._source[id].remove(value)\nif (ctx._source[id].size() == 0) ctx._source.remove(id) } }"
}
