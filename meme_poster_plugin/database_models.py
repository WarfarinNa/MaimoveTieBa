"""
Meme发送插件数据库模型
"""

from peewee import *
from src.common.database.database_model import BaseModel


class MemeSendRecords(BaseModel):
    """Meme发送记录表"""
    
    # 基本信息
    group_id = CharField(max_length=50, help_text="群组ID")
    group_name = CharField(max_length=100, help_text="群组名称")
    send_date = CharField(max_length=10, help_text="发送日期 YYYY-MM-DD")
    send_time = CharField(max_length=20, help_text="发送时间")
    
    # 内容信息
    post_title = CharField(max_length=200, help_text="帖子标题")
    post_content = TextField(null=True, help_text="帖子内容")
    post_author = CharField(max_length=50, null=True, help_text="帖子作者")
    image_count = IntegerField(default=0, help_text="图片数量")
    
    # 状态信息
    send_success = BooleanField(default=True, help_text="发送是否成功")
    error_message = TextField(null=True, help_text="错误信息")
    
    # 时间戳
    created_at = DateTimeField(auto_now_add=True, help_text="创建时间")
    
    class Meta:
        table_name = 'meme_send_records'
        indexes = (
            # 按群组和日期查询
            (('group_id', 'send_date'), False),
            # 按日期查询
            (('send_date',), False),
        )


class MemeContentCache(BaseModel):
    """Meme内容缓存表"""
    
    # 内容标识
    content_id = CharField(max_length=100, unique=True, help_text="内容唯一标识")
    source = CharField(max_length=50, help_text="内容来源（如：tieba）")
    source_id = CharField(max_length=100, help_text="来源ID")
    
    # 内容信息
    title = CharField(max_length=200, help_text="标题")
    content = TextField(null=True, help_text="内容")
    author = CharField(max_length=50, null=True, help_text="作者")
    images = TextField(null=True, help_text="图片URL列表（JSON格式）")
    
    # 分类信息
    is_meme = BooleanField(default=False, help_text="是否为meme内容")
    meme_score = FloatField(default=0.0, help_text="meme评分")
    tags = TextField(null=True, help_text="标签（JSON格式）")
    
    # 使用统计
    send_count = IntegerField(default=0, help_text="发送次数")
    last_send_time = DateTimeField(null=True, help_text="最后发送时间")
    
    # 时间戳
    created_at = DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = DateTimeField(auto_now=True, help_text="更新时间")
    
    class Meta:
        table_name = 'meme_content_cache'
        indexes = (
            # 按来源查询
            (('source', 'source_id'), False),
            # 按meme状态查询
            (('is_meme',), False),
            # 按评分查询
            (('meme_score',), False),
        )


class MemeGroupSettings(BaseModel):
    """群组设置表"""
    
    # 群组信息
    group_id = CharField(max_length=50, unique=True, help_text="群组ID")
    group_name = CharField(max_length=100, help_text="群组名称")
    
    # 发送设置
    enabled = BooleanField(default=True, help_text="是否启用")
    max_daily_sends = IntegerField(default=3, help_text="每日最大发送次数")
    send_interval_min = IntegerField(default=30, help_text="发送间隔（分钟）")
    
    # 内容过滤
    allowed_keywords = TextField(null=True, help_text="允许的关键词（JSON格式）")
    blocked_keywords = TextField(null=True, help_text="屏蔽的关键词（JSON格式）")
    
    # 时间设置
    active_hours = TextField(null=True, help_text="活跃时间段（JSON格式）")
    
    # 时间戳
    created_at = DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = DateTimeField(auto_now=True, help_text="更新时间")
    
    class Meta:
        table_name = 'meme_group_settings'
        indexes = (
            # 按群组ID查询
            (('group_id',), False),
        )
