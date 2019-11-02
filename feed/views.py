from .models import Post, Comment, PostSerializer, CommentSerializer, Feed
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PostListCreateAPIView(APIView):
    def get(self, request, feed_id):
        """
            피드의 게시물 리스트 불러오는 API

            ---
            # Path Params
                - feed_id : 피드 id
            # Response
                - id : 게시물 id
                - content : 게시물 내용
                - image : image url
                - created_at : 작성시간
                - updated_at : 수정시간
                - feed : 피드 id
                - author : 작성자 id
        """
        posts = Feed.objects.prefetch_related('post_set').get(id=feed_id).post_set.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, feed_id):
        """
            피드에 게시물 등록 API

            ---
            # Path Params
                - feed : 피드 id
            # Body
                - author : 작성자 id(Required)
                - content : 게시물 내용(Required)
                - image : image 객체
            # Response
                - id : 게시물 id
                - content : 게시물 내용
                - image : image url
                - created_at : 작성시간
                - updated_at : 수정시간
                - feed : 피드 id
                - author : 작성자 id
        """
        request.data['feed'] = feed_id
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        게시물 조회 & 수정 & 삭제 API

        ---
        # Path Params
            - feed_id : 피드 id
            - id : 게시물 id
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


def like_post(request, feed_id, post_id):
    # """
    #     게시물 좋아요 API
    #
    #     ---
    #     # Path Params
    #         - feed_id : 피드 id
    #         - post_id : 게시물 id
    # """
    # try:
    #     post = Post.objects.get(id=post_id)
    #     # request.user.username = post.author.username
    #     # request.user = post.author
    #     print(post.likes.name)
    #     print(post.like_count)
    #     if post:
    #         # if post.likes.filter(username=request.user.username).exists:
    #         #     print(post.likes)
    #         #     print(request.user.username)
    #         #     print('hi')
    #         #     post.likes.remove(request.user)
    #         # else:
    #         #     print('bye')
    #         #     post.likes.add(request.user)
    #         # post.likes.remove(request.user)
    #         # post.likes.add(request.user)
    #         return Response()
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    # except:
    #     return Response()
    pass


class CommentListCreateAPIView(APIView):
    def get(self, request, feed_id, post_id):
        """
            게시물의 댓글 리스트 불러오는 API

            ---
            # Path Params
                - feed_id : 피드 id
                - post_id : 게시물 id
            # Response
                - id : 댓글 id,
                - content : 댓글 내용,
                - created_at : 작성시간,
                - updated_at : 수정시간,
                - post : 게시물 id,
                - author : 작성자 id
        """
        comments = Post.objects.prefetch_related('comment_set').get(id=post_id).comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, feed_id, post_id):
        """
            게시물에 댓글 등록하는 API

            ---
            # Path Params
                - feed_id : 피드 id
                - post_id : 게시물 id
            # Body
                - author : 작성자 id(Required)
                - content : 댓글 내용(Required)
            # Response
                - id : 댓글 id,
                - content : 댓글 내용,
                - created_at : 작성시간,
                - updated_at : 수정시간,
                - post : 게시물 id,
                - author : 작성자 id
        """
        request.data['post'] = post_id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        댓글 조회 & 수정 & 삭제 API

        ---
        # Path Params
            - feed_id : 피드 id
            - post_id : 게시물 id
            - id : 댓글 id
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
