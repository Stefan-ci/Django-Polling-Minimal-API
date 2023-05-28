from polls.models import Poll, Answer
from rest_framework import serializers



class AnswerSerializer(serializers.ModelSerializer):
    poll = serializers.ReadOnlyField(source="poll.question")
    poll_id = serializers.ReadOnlyField(source="poll.id")
    
    class Meta:
        model = Answer
        fields = ["id", "poll", "poll_id", "answer", "is_active", "created_on", "extra_data"]


        

class PollListSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Poll
        fields = ["id", "question", "slug", "is_active", "created_on", "detail_url"]
    
    def get_detail_url(self, obj):
        return obj.get_absolute_url()
    




class PollSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)
    answers = serializers.SerializerMethodField(read_only=True)
    answers_count = serializers.SerializerMethodField(read_only=True)
    similar_polls = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Poll
        fields = ["id", "question", "slug", "is_active", "created_on", "answers_count", "detail_url",
            "extra_data", "answers", "similar_polls"]
    
    
    def get_detail_url(self, obj):
        return obj.get_absolute_url()

    def get_answers_count(self, obj):
        return obj.count_active_answers()
    
    def get_answers(self, obj):
        return AnswerSerializer(obj.answers(), many=True).data
    
    def get_similar_polls(self, obj):
        return PollListSerializer(obj.similar_polls(), many=True).data



class CreatePollSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=255)
    answers = serializers.ListField(min_length=1)
