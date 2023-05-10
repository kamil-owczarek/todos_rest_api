from src.service import services
from src.domain.model import ItemSchema


def test_get_item(fake_uow):
    result = services.get_item(1, fake_uow)
    assert result.id == 1
    assert result.title == "test title"
    assert result.description == "test description"
    assert result.completed == False


def test_get_items(fake_uow):
    results = services.get_items(fake_uow)
    assert results[0].id == 1
    assert results[0].title == "test title"
    assert results[0].description == "test description"
    assert results[0].completed == False
    assert results[1].id == 2
    assert results[1].title == "dummy title"
    assert results[1].description == "dummy description"
    assert results[1].completed == True


def test_insert_item(fake_uow):
    item = ItemSchema(id=3, title="new", description="new", completed=True)
    services.insert_item(item, fake_uow)
    result = services.get_item(3, fake_uow)
    assert result.id == 3
    assert result.title == "new"
    assert result.description == "new"
    assert result.completed == True


def test_update_item(fake_uow):
    item = ItemSchema(id=1, title="updated", description="updated", completed=True)
    services.update_item(1, item, fake_uow)
    result = services.get_item(1, fake_uow)
    assert result.id == 1
    assert result.title == "updated"
    assert result.description == "updated"
    assert result.completed == True


def test_delete_item(fake_uow):
    expected_length = len(services.get_items(fake_uow)) - 1
    delete_record = services.get_item(2, fake_uow)
    services.delete_item(2, fake_uow)
    result = services.get_items(fake_uow)
    assert len(result) == expected_length
    assert delete_record not in result
