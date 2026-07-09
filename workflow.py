from gmail_client import GmailClient
from gemini_client import GeminiClient
from slack_client import SlackClient
from database import SessionLocal
from models import EmailRecord, EmailCategory
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Workflow:
    def __init__(self):
        self.gmail = GmailClient()
        self.gemini = GeminiClient()
        self.slack = SlackClient()

    def process_new_emails(self):
        """Main workflow: fetch unread emails, classify, route, and act."""
        messages = self.gmail.get_unread_messages()
        if not messages:
            logger.info("No new unread emails.")
            return

        for msg_meta in messages:
            msg_id = msg_meta['id']
            try:
                self._process_single_email(msg_id)
            except Exception as e:
                logger.error(f"Error processing email {msg_id}: {e}")

    def _process_single_email(self, msg_id):
        # 1. Fetch full email
        msg = self.gmail.get_message(msg_id)
        email_data = self.gmail.extract_email_data(msg)

        # 2. Classify with Gemini
        classification = self.gemini.classify_email(
            subject=email_data['subject'],
            body=email_data['body']
        )
        category = classification['category']
        confidence = classification['confidence']
        logger.info(f"Email {msg_id} classified as {category} with confidence {confidence}")

        # 3. Save to database (always)
        db = SessionLocal()
        record = EmailRecord(
            gmail_message_id=email_data['gmail_message_id'],
            subject=email_data['subject'],
            sender=email_data['sender'],
            body=email_data['body'],
            category=EmailCategory[category.upper()],
            confidence=confidence
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        # 4. Route based on category
        if category == 'high_priority':
            self._handle_high_priority(msg_id, email_data, record)
        elif category == 'customer_support':
            self._handle_customer_support(msg_id, email_data, record)
        elif category == 'newsletter':
            self._handle_newsletter(msg_id, email_data, record)
        elif category == 'spam':
            self._handle_spam(msg_id, email_data, record)
        else:
            self._handle_other(msg_id, email_data, record)

        db.close()

    def _handle_high_priority(self, msg_id, email_data, record):
        # Auto-reply
        reply_msg = "Thank you for your email. This is an automated response acknowledging your high-priority message. Our team will contact you shortly."
        self.gmail.send_reply(msg_id, reply_msg)
        record.auto_replied = 1

        # Slack notification
        slack_text = f"🚨 *High Priority Email*\nFrom: {email_data['sender']}\nSubject: {email_data['subject']}\nMessage ID: {msg_id}"
        self.slack.send_notification(slack_text)
        record.slack_notified = 1

        # Archive
        self.gmail.archive_message(msg_id)
        record.archived = 1

        # Add label (optional)
        self.gmail.add_label(msg_id, 'HighPriority')

        # Update record
        db = SessionLocal()
        db.merge(record)
        db.commit()
        db.close()
        logger.info(f"High-priority email {msg_id} handled.")

    def _handle_customer_support(self, msg_id, email_data, record):
        # Auto-reply
        reply_msg = "Thank you for contacting support. We have received your query and will get back to you within 24 hours."
        self.gmail.send_reply(msg_id, reply_msg)
        record.auto_replied = 1

        # Store in database (already stored, but we can mark as support)
        self.gmail.add_label(msg_id, 'Support')

        # Optionally archive after reply? Usually keep in inbox for agents
        # Not archiving, but could be archived later. We'll leave in inbox.

        db = SessionLocal()
        db.merge(record)
        db.commit()
        db.close()
        logger.info(f"Customer support email {msg_id} handled.")

    def _handle_newsletter(self, msg_id, email_data, record):
        # Archive and label
        self.gmail.archive_message(msg_id)
        self.gmail.add_label(msg_id, 'Newsletter')
        record.archived = 1

        db = SessionLocal()
        db.merge(record)
        db.commit()
        db.close()
        logger.info(f"Newsletter email {msg_id} archived.")

    def _handle_spam(self, msg_id, email_data, record):
        # Delete permanently
        self.gmail.delete_message(msg_id)
        # We might also want to remove from DB or mark as deleted
        db = SessionLocal()
        db.delete(record)
        db.commit()
        db.close()
        logger.info(f"Spam email {msg_id} deleted.")

    def _handle_other(self, msg_id, email_data, record):
        # For other, just archive? Or leave in inbox
        self.gmail.archive_message(msg_id)
        self.gmail.add_label(msg_id, 'Other')
        record.archived = 1

        db = SessionLocal()
        db.merge(record)
        db.commit()
        db.close()
        logger.info(f"Other email {msg_id} archived.")