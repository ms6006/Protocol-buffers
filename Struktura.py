import messages_pb2 as m

req = m.Request()
res = m.Response()

def check_id(parent):
    for i in req.steps:
        if i.name == parent.name and i.duration == parent.duration:
            return i.id

def create_children(parent, id):
    for i in req.steps:
        if i.parent_id == id:
            t = parent.children.add()
            t.name = i.name
            t.duration = i.duration

def sort_children(parent):
    i = 0
    while i < len(parent.children)-1:
        if parent.children[i].duration < parent.children[i+1].duration:
            t = parent.children[i].name
            f = parent.children[i].duration
            parent.children[i].duration = parent.children[i+1].duration
            parent.children[i].name = parent.children[i+1].name
            parent.children[i + 1].name = t
            parent.children[i + 1].duration = f
            i = 0
        else: i = i + 1

def create_children_for_children(parent):
    for i in parent.children:
        id = check_id(i)
        create_children(i, id)
        sort_children(i)
        create_children_for_children(i)

def max_duration(parent):
    max = parent.duration
    for i in parent.children:
        max = max - i.duration
        max_duration(i)

    if max > res.max_duration_step_duration:
        res.max_duration_step_duration = max
        res.max_duration_step_name = parent.name

def main(request):
    req.ParseFromString(request)

    first = res.hierarchical_step
    id = 0
    if req.step_id != 0:
        for i in req.steps:
            if i.id == req.step_id:
                id = i.id
                first.name = i.name
                first.duration = i.duration
                break
    else:
        for i in req.steps:
            if i.parent_id == 0:
                id = i.id
                first.name = i.name
                first.duration = i.duration
                break

    create_children(first, id)
    sort_children(first)
    create_children_for_children(first)
    max_duration(first)

    return (res.SerializeToString())

if __name__ == '__main__':
    request = b'\n\x08\x08\x01\x18\x96\x01"\x01A\n\t\x08\x02\x10\x01\x18-"\x01B\n\t\x08\x03\x10\x01\x182"\x01C\n\t\x08\x04\x10\x02\x18\x14"\x01D\n\t\x08\x05\x10\x02\x18\x14"\x01E\x10\x01'
    response = main(request)
    #print(req)
    #print(res)
    print(response)


