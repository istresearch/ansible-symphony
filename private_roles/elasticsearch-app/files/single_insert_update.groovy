{
    "script": "for (item in myArray) { String id = item.get(\"id\")\nString value = item.get(\"value\")\nctx._source[id] = value }"
}
