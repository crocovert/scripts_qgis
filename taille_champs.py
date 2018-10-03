##layer=vector

table=processing.getObject(layer)
table.startEditing()
table.dataProvider().fields().field('ref').setLength(20)
table.updateFields()
table.commitChanges()
print(table.dataProvider().fields().field('ref').length())
