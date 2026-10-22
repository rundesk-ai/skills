+++
skill = "writing-bug-tickets"
kind = "routing"
expect = "no-fire"
rubric = "Debugging work, not writing a report: neither ticket skill loads."
+++
This function returns the wrong total when the cart has a discount and free shipping together. Find out why and tell me the fix:

def total(items, discount, free_shipping):
    subtotal = sum(i["price"] * i["qty"] for i in items)
    shipping = 0 if free_shipping else 5
    return subtotal - discount * subtotal + shipping if discount < 1 else subtotal - discount + shipping
