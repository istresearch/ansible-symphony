{
    "script": "for (item in myArray) { String id = item.get(\"id\")\nString value = item.get(\"value\")\nif (ctx._source.containsKey(id)) { if (ctx._source[id].contains(value) == false) ctx._source[id] += value } else { ctx._source[id] = [value] } }"
}
