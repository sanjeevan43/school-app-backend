-- Ensure only ONE FCM token per parent_id for Single Device Login
-- This migration adds a unique constraint on the parent_id column in fcm_tokens table

-- First, clean up any existing duplicate tokens (keep the latest updated one)
DELETE t1 FROM fcm_tokens t1
INNER JOIN fcm_tokens t2 
WHERE t1.updated_at < t2.updated_at 
AND t1.parent_id = t2.parent_id 
AND t1.parent_id IS NOT NULL;

-- Add the unique constraint
ALTER TABLE fcm_tokens ADD UNIQUE INDEX idx_unique_parent_fcm (parent_id);
