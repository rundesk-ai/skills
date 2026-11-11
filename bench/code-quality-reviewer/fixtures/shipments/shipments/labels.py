"""The text printed on a parcel's label."""


def label_text(row, customer):
    delivery_address = row["drop_point"]
    lines = [customer["name"], delivery_address, "%d g" % row["weight"]]
    return "\n".join(lines)
