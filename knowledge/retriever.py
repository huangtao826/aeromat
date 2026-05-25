"""知识库检索器"""
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional


class KnowledgeRetriever:
    """知识库检索器 - 从文档和FAQ中检索相关内容"""

    def __init__(self, knowledge_dir: Optional[Path] = None):
        if knowledge_dir is None:
            # 开发模式下使用源码目录
            source_dir = Path(__file__).parent

            # 打包模式下优先从 exe 同目录读取（支持用户扩展）
            if getattr(sys, 'frozen', False):
                base_dir = Path(sys._MEIPASS)
                external_knowledge = Path(sys.executable).parent / "knowledge"
                if external_knowledge.exists():
                    knowledge_dir = external_knowledge
                else:
                    knowledge_dir = base_dir / "knowledge"
            else:
                knowledge_dir = source_dir

        self.knowledge_dir = Path(knowledge_dir)
        self.docs_dir = self.knowledge_dir / "docs"
        self.faqs_dir = self.knowledge_dir / "faqs"

    def retrieve(self, query: str, top_k: int = 3, source: str = "all") -> List[Dict]:
        """
        根据查询检索相关知识

        Args:
            query: 用户查询
            top_k: 返回前k条结果
            source: "docs" | "faqs" | "all"

        Returns:
            List of relevant knowledge items with content and metadata
        """
        results = []

        if source in ["docs", "all"]:
            results.extend(self._search_docs(query))

        if source in ["faqs", "all"]:
            results.extend(self._search_faqs(query))

        # 按相关性排序
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:top_k]

    def _search_docs(self, query: str) -> List[Dict]:
        """搜索文档库"""
        results = []
        docs_dir = self.docs_dir

        if not docs_dir.exists():
            return results

        keywords = self._extract_keywords(query)

        for doc_file in docs_dir.glob("*.md"):
            content = doc_file.read_text(encoding="utf-8")
            relevance = self._calculate_relevance(query, keywords, content)

            if relevance > 0:
                results.append({
                    "type": "doc",
                    "title": doc_file.stem.replace("_", " ").title(),
                    "file": str(doc_file.name),
                    "content": content[:500],  # 摘要前500字符
                    "full_content": content,
                    "relevance": relevance
                })

        return results

    def _search_faqs(self, query: str) -> List[Dict]:
        """搜索FAQ库"""
        results = []
        faqs_dir = self.faqs_dir

        if not faqs_dir.exists():
            return results

        keywords = self._extract_keywords(query)

        for faq_file in faqs_dir.glob("*.md"):
            content = faq_file.read_text(encoding="utf-8")
            relevance = self._calculate_relevance(query, keywords, content)

            if relevance > 0:
                results.append({
                    "type": "faq",
                    "title": faq_file.stem.replace("_", " ").title(),
                    "file": str(faq_file.name),
                    "content": content[:300],
                    "full_content": content,
                    "relevance": relevance
                })

        return results

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 移除标点符号，分割文本
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        # 过滤停用词
        stopwords = {'的', '是', '在', '了', '和', '与', '或', '如何', '怎么', '什么', '为什么'}
        return [w for w in words if len(w) >= 2 and w not in stopwords]

    def _calculate_relevance(self, query: str, keywords: List[str], content: str) -> float:
        """计算相关性分数"""
        content_lower = content.lower()
        score = 0.0

        # 精确匹配查询
        if query.lower() in content_lower:
            score += 5.0

        # 关键词匹配
        for keyword in keywords:
            if keyword in content_lower:
                score += 1.0
                # 多次出现加分
                count = content_lower.count(keyword)
                score += min(count * 0.5, 2.0)

        return score

    def format_results(self, results: List[Dict]) -> str:
        """格式化检索结果为文本"""
        if not results:
            return ""

        formatted = []
        for i, item in enumerate(results, 1):
            if item["type"] == "doc":
                formatted.append(f"📄 **{item['title']}**\n{item['content']}...")
            elif item["type"] == "faq":
                formatted.append(f"❓ **{item['title']}**\n{item['content']}...")

        return "\n\n".join(formatted)