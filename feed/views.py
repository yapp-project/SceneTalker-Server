from .models import Post, Comment, PostSerializer, CommentSerializer, Feed
from django.http import JsonResponse
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
                - is_mine : 사용자가 작성했는지 여부
                - is_liked_by_me : 사용자가 좋아요를 눌렀는지 여부
                - content : 게시물 내용
                - image : image url
                - created_at : 작성시간
                - updated_at : 수정시간
                - feed : 피드 id
                - author : 작성자 id
        """
        posts = Feed.objects.prefetch_related('post_set').get(id=feed_id).post_set.all()
        serializer = PostSerializer(posts, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request, feed_id):
        """
            피드에 게시물 등록 API

            ---
            # Path Params
                - feed : 피드 id
            # Body
                - content : 게시물 내용(Required)
                - image : image 객체
            # Response
                - id : 게시물 id
                - is_mine : 사용자가 작성했는지 여부
                - is_liked_by_me : 사용자가 좋아요를 눌렀는지 여부
                - content : 게시물 내용
                - image : image url
                - created_at : 작성시간
                - updated_at : 수정시간
                - feed : 피드 id
                - author : 작성자 id
        """
        request.data['feed'] = feed_id
        request.data['author'] = request.user.id
        serializer = PostSerializer(data=request.data, context={'request': request})
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


class PostLikesUpdateAPIView(APIView):
    """
        게시물 좋아요 API

        ---
        # Path Params
            - feed_id : 피드 id
            - post_id : 게시물 id
    """
    def post(self, request, feed_id, post_id):
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return Response()


class CommentListCreateAPIView(APIView):
    def get(self, request, feed_id, post_id):
        """
            게시물의 댓글 리스트 불러오는 API

            ---
            # Path Params
                - feed_id : 피드 id
                - post_id : 게시물 id
            # Response
                - id : 댓글 id
                - is_mine : 사용자가 작성했는지 여부
                - is_liked_by_me : 사용자가 좋아요를 눌렀는지 여부
                - like_counts : 좋아요 개수
                - content : 댓글 내용
                - created_at : 작성시간
                - updated_at : 수정시간
                - post : 게시물 id
                - author : 작성자 id
        """
        comments = Post.objects.prefetch_related('comment_set').get(id=post_id).comment_set.all()
        serializer = CommentSerializer(comments, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request, feed_id, post_id):
        """
            게시물에 댓글 등록하는 API

            ---
            # Path Params
                - feed_id : 피드 id
                - post_id : 게시물 id
            # Body
                - content : 댓글 내용(Required)
            # Response
                - id : 댓글 id,
                - is_mine : 사용자가 작성했는지 여부
                - is_liked_by_me : 사용자가 좋아요를 눌렀는지 여부
                - content : 댓글 내용,
                - created_at : 작성시간,
                - updated_at : 수정시간,
                - post : 게시물 id,
                - author : 작성자 id
        """
        request.data['post'] = post_id
        request.data['author'] = request.user.id
        serializer = CommentSerializer(data=request.data, context={'request': request})
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
