from .linkDAO import LinkDAO
from ..dependencies import generate_string

class LinkRepository:
    def __init__(self):
        self.linkDAO = LinkDAO()

    def add_link(self, original_url, short_alias):
        if short_alias == "":
            short_alias = generate_string()
        self.linkDAO.create_link(original_url, short_alias)

    def take_url_of_alias(self, short_alias: str):
        res = self.linkDAO.get_url_by_alias(short_alias)
        self.linkDAO.update_clicks(res[1], short_alias)
        return res[0]

    def delete_link(self, id):
        self.linkDAO.delete_by_id(id)

    def show_all_links(self):
        return self.linkDAO.get_all_links()