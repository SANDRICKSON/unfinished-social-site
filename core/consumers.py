import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Post, Like
from .serializers import PostSerializer

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'likes_{self.post_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive like action from user
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']  # like or unlike
        post = Post.objects.get(id=self.post_id)

        # Handle the like/unlike action
        if action == 'like':
            like, created = Like.objects.get_or_create(user=self.user, post=post)
        elif action == 'unlike':
            Like.objects.filter(user=self.user, post=post).delete()

        # Get updated like count
        updated_like_count = post.like_count

        # Broadcast new like count to WebSocket clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_like_count',
                'like_count': updated_like_count
            }
        )

    # Send updated like count to WebSocket clients
    async def send_like_count(self, event):
        like_count = event['like_count']
        await self.send(text_data=json.dumps({
            'like_count': like_count
        }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Post, Like
from .serializers import PostSerializer

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'likes_{self.post_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive like action from user
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']  # like or unlike
        post = Post.objects.get(id=self.post_id)

        # Handle the like/unlike action
        if action == 'like':
            like, created = Like.objects.get_or_create(user=self.user, post=post)
        elif action == 'unlike':
            Like.objects.filter(user=self.user, post=post).delete()

        # Get updated like count
        updated_like_count = post.like_count

        # Broadcast new like count to WebSocket clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_like_count',
                'like_count': updated_like_count
            }
        )

    # Send updated like count to WebSocket clients
    async def send_like_count(self, event):
        like_count = event['like_count']
        await self.send(text_data=json.dumps({
            'like_count': like_count
        }))
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Post, Comment, Reply
from .serializers import CommentSerializer, ReplySerializer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'comments_{self.post_id}'

        # Adding the user to the comment group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive comment or reply action
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']  # comment or reply
        post = Post.objects.get(id=self.post_id)

        if action == 'comment':
            content = data['content']
            comment = Comment.objects.create(user=self.user, post=post, content=content)
            comment_serializer = CommentSerializer(comment)

            # Send the new comment to all group members
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_comment',
                    'comment': comment_serializer.data
                }
            )
        elif action == 'reply':
            content = data['content']
            comment_id = data['comment_id']
            comment = Comment.objects.get(id=comment_id)
            reply = Reply.objects.create(user=self.user, comment=comment, content=content)
            reply_serializer = ReplySerializer(reply)

            # Send the new reply to all group members
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_reply',
                    'reply': reply_serializer.data
                }
            )

    # Send a new comment to WebSocket clients
    async def send_comment(self, event):
        comment = event['comment']
        await self.send(text_data=json.dumps({
            'type': 'comment',
            'comment': comment
        }))

    # Send a new reply to WebSocket clients
    async def send_reply(self, event):
        reply = event['reply']
        await self.send(text_data=json.dumps({
            'type': 'reply',
            'reply': reply
        }))
