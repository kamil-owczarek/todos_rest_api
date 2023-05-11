from src.domain.schema import ItemSchema


def test_item_creation_from_dict_row(test_items):
    results = [ItemSchema(**row._asdict()) for row in test_items]
    assert isinstance(results[0], ItemSchema)
    assert isinstance(results[1], ItemSchema)
    assert results[0].id == 1
    assert results[0].title == "test title"
    assert results[0].description == "test description"
    assert results[0].completed == False
    assert results[1].id == 2
    assert results[1].title == "dummy title"
    assert results[1].description == "dummy description"
    assert results[1].completed == True
