class TaskName(object):
    def __init__(self, action=None, main_entity=None, secondary_entity=None):
        self.action = action
        self.main_entity = main_entity
        self.secondary_entity = secondary_entity

    def __eq__(self, other):
        return (
            self.action == other.action
            and self.main_entity == other.main_entity
            and self.secondary_entity == other.secondary_entity
        )

    def __repr__(self):
        return f"TaskName({self.action}, {self.main_entity}, {self.secondary_entity})"


class TaskNameParser(object):
    def parse(self, str_name):
        # "add_activity_to_perspective"
        words = str_name.split("_")
        entities = self._split_by_preposition(words)
        main_entity = entities[0].strip().title()
        if len(entities) == 2:
            secondary_entity = entities[1].strip().capitalize()
        else:
            secondary_entity = None
        return TaskName(
            action=words[0].capitalize(),
            main_entity=main_entity,
            secondary_entity=secondary_entity,
        )

    def _split_by_preposition(self, words):
        entities = " ".join(words[1:]).split(self._find_entity_delimiter(words))
        result = []
        join_prepositions = ["for", "with"]
        for entity in entities:
            # entity="agent for development","perspective with seq_no"
            for join_prep in join_prepositions:
                entity_name = entity.split(join_prep)[0]
                if join_prep in entity:
                    break

            result.append(entity_name)
        return result

    def _find_entity_delimiter(self, words):
        delimiters = ["to", "from"]
        for delimiter in delimiters:
            if delimiter in words:
                return delimiter
        return "xxxxxx"  # some weird delimiter so it doesnt split
