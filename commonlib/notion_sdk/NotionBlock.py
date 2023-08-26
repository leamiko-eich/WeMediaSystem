#encoding=utf-8

class NotionBlock(object):
    def __init__(self):
        pass


    def add_head_json(self, ori_title):

        cnt = ori_title.count("#")
        title = ori_title.replace("#", "")
        # print("ori:%s title:%s cnt:%d" %(ori_title, title, cnt))

        if cnt==2:
            json_block = \
                {
                    "object": "block",
                    "id": "15989be4-1d3a-4bb9-98a2-9491fe296664",
                    "parent": {
                        "type": "page_id",
                        "page_id": "df1ea4e1-ae47-4129-bc0e-102505397c3e"
                    },
                    "created_time": "2023-05-24T12:36:00.000Z",
                    "last_edited_time": "2023-05-24T12:36:00.000Z",
                    "created_by": {
                        "object": "user",
                        "id": "b41fa192-a04a-4ca9-8c54-74da48c8e220"
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "b41fa192-a04a-4ca9-8c54-74da48c8e220"
                    },
                    "has_children": False,
                    "archived": False,
                    "type": "heading_2",
                    "heading_2": {
                        "is_toggleable": False,
                        "color": "default",
                        "text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": title,
                                    "link": None
                                },
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "default"
                                },
                                "plain_text": title,
                                "href": None
                            }
                        ]
                    }
                }
        elif cnt==1:
            json_block = \
                {
                    "object": "block",
                    "id": "15989be4-1d3a-4bb9-98a2-9491fe296664",
                    "parent": {
                        "type": "page_id",
                        "page_id": "df1ea4e1-ae47-4129-bc0e-102505397c3e"
                    },
                    "created_time": "2023-05-24T12:36:00.000Z",
                    "last_edited_time": "2023-05-24T12:36:00.000Z",
                    "created_by": {
                        "object": "user",
                        "id": "b41fa192-a04a-4ca9-8c54-74da48c8e220"
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "b41fa192-a04a-4ca9-8c54-74da48c8e220"
                    },
                    "has_children": False,
                    "archived": False,
                    "type": "heading_1",
                    "heading_1": {
                        "is_toggleable": False,
                        "color": "default",
                        "text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": title,
                                    "link": None
                                },
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "default"
                                },
                                "plain_text": title,
                                "href": None
                            }
                        ]
                    }
                }
        elif cnt==3:
            json_block = \
                {
                    "object": "block",
                    "id": "15989be4-1d3a-4bb9-98a2-9491fe296664",
                    "parent": {
                        "type": "page_id",
                        "page_id": "df1ea4e1-ae47-4129-bc0e-102505397c3e"
                    },
                    "created_time": "2023-05-24T12:36:00.000Z",
                    "last_edited_time": "2023-05-24T12:36:00.000Z",
                    "created_by": {
                        "object": "user",
                        "id": "b41fa192-a04a-4ca9-8c54-74da48c8e220"
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "b41fa192-a04a-4ca9-8c54-74da48c8e220"
                    },
                    "has_children": False,
                    "archived": False,
                    "type": "heading_2",
                    "heading_2": {
                        "is_toggleable": False,
                        "color": "default",
                        "text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": title,
                                    "link": None
                                },
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "default"
                                },
                                "plain_text": title,
                                "href": None
                            }
                        ]
                    }
                }
        else:
            json_block = \
                {
                    "object": "block",
                    "id": "32564298-4a2e-441b-b482-41c202611d07",
                    "parent": {
                        "type": "page_id",
                        "page_id": "df1ea4e1-ae47-4129-bc0e-102505397c3e"
                    },
                    "created_time": "2023-05-24T12:36:00.000Z",
                    "last_edited_time": "2023-05-24T12:36:00.000Z",
                    "created_by": {
                        "object": "user",
                        "id": "b41fa192-a04a-4ca9-8c54-74da48c8e220"
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "b41fa192-a04a-4ca9-8c54-74da48c8e220"
                    },
                    "has_children": False,
                    "archived": False,
                    "type": "paragraph",
                    "paragraph": {
                        "color": "default",
                        "text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": title,
                                    "link": None
                                },
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "default"
                                },
                                "plain_text": title,
                                "href": None
                            }
                        ]
                    }
                } 


        return json_block

    