import sys

from src import configuration


# noinspection PyProtectedMember
def single_thread(table, cursor, cls) -> int:
    args = []

    for data in cursor:
        entity = cls(table, data)
        entity.generate()
        if entity.modified:
            args.append(entity.data)

    if configuration.DEBUG:
        print('args', args)

    if len(args):

        query = "UPDATE {} SET {} WHERE {}".format(
            table.name,
            ", ".join("{0}=%({0})s".format(g) for g in table.generated_fields),
            " AND ".join("{0}=%({0})s".format(p) for p in table.primary_fields)
        )

        affected = table._executemany(query, args).result

        if len(args) != affected:
            if configuration.DEBUG:
                print("Pocet args: {}, pocet affected: {}".format(len(args), affected), file=sys.stderr)
            affected = affected or 0

        return affected

    else:
        return 0
