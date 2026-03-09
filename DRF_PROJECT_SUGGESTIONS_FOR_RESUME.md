# 🚀 Django REST Framework - Resume-Worthy Project Suggestions

> **Goal:** Single-app projects perfect for internship resumes that showcase your DRF skills

Each project has **1 main app + 1 user role** (Admin already exists by default)

---

## 📌 Project 1: Task Management API (Recommended ⭐)

### 🎯 Why This Project?
- **Simple but Powerful**: Shows full CRUD operations
- **Real-world Use**: Everyone uses task managers
- **Great for Interviews**: Easy to explain and demo
- **Tech Showcase**: Authentication, permissions, filtering, search

### 📱 Project Overview
A RESTful API for personal task management where users can create, manage, and organize their daily tasks with categories, priorities, and deadlines.

### 🏗️ App Structure
**Single App:** `tasks`

**User Role:** `Regular User` (owner of their tasks)

### 📊 Models

#### **CustomUser Model**
- email (unique, required)
- username
- is_active
- date_joined

#### **Category Model**
- user (ForeignKey - each user has their own categories)
- name (CharField)
- color (CharField - hex code for UI)
- icon (CharField - emoji or icon name)
- created_at

#### **Task Model**
- user (ForeignKey - task owner)
- title (CharField)
- description (TextField, optional)
- category (ForeignKey to Category, optional)
- priority (CharField: choices - 'low', 'medium', 'high', 'urgent')
- status (CharField: choices - 'todo', 'in_progress', 'completed', 'archived')
- due_date (DateTimeField, optional)
- completed_at (DateTimeField, null)
- is_important (BooleanField)
- created_at
- updated_at

#### **SubTask Model** (Optional - shows nested relationships)
- task (ForeignKey to Task)
- title (CharField)
- is_completed (BooleanField)
- order (IntegerField)

### 🔐 Permissions
- **IsOwner**: Users can only see/edit their own tasks
- **IsAuthenticated**: All endpoints require login

### 🎯 Views Structure (CRUD vs Logical)

> **Legend:** 🔵 = CRUD View | 🟢 = Logical View

#### **Authentication Views**

##### 🟢 **UserRegistrationView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** AllowAny
- **Logic:**
  - Validate email uniqueness
  - Hash password
  - Create user instance
  - Send verification email (optional)
  - Return JWT tokens

##### 🟢 **UserLoginView** (LOGICAL - TokenObtainPairView)
- **Method:** POST
- **Permission:** AllowAny
- **Logic:**
  - Validate credentials
  - Check user is_active
  - Generate JWT access & refresh tokens
  - Return tokens with user info

##### 🟢 **UserLogoutView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Logic:**
  - Blacklist refresh token
  - Return success message

##### 🔵 **UserProfileView** (CRUD - RetrieveUpdateAPIView)
- **Methods:** GET, PUT, PATCH
- **Permission:** IsAuthenticated
- **Description:** Get/update current user profile

---

#### **Category Views**

##### 🔵 **CategoryListCreateView** (CRUD - ListCreateAPIView)
- **Methods:** GET, POST
- **Permission:** IsAuthenticated
- **Filtering:** None (shows only user's categories via queryset filter)
- **Description:** List and create categories for logged-in user

##### 🔵 **CategoryDetailView** (CRUD - RetrieveUpdateDestroyAPIView)
- **Methods:** GET, PUT, PATCH, DELETE
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Manage specific category

##### 🟢 **CategoryTasksView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated + IsOwner
- **Logic:**
  - Get all tasks belonging to specific category
  - Filter by user (only owner's tasks)
  - Return tasks with count

---

#### **Task Views**

##### 🔵 **TaskListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Filtering:**
  - `status` (choices: 'todo', 'in_progress', 'completed', 'archived')
  - `priority` (choices: 'low', 'medium', 'high', 'urgent')
  - `category` (by category ID)
  - `is_important` (boolean)
  - `due_date` (date or date range)
  - `search` (title, description)
- **Ordering:** -created_at, due_date, priority, -updated_at  
- **Pagination:** PageNumberPagination (20 per page)
- **Description:** List all user's tasks with advanced filtering

##### 🔵 **TaskCreateView** (CRUD - CreateAPIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Description:** Create new task (automatically sets user as owner)

##### 🔵 **TaskDetailView** (CRUD - RetrieveAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Get specific task details

##### 🔵 **TaskUpdateView** (CRUD - UpdateAPIView)
- **Methods:** PUT, PATCH
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Update task details

##### 🔵 **TaskDeleteView** (CRUD - DestroyAPIView)
- **Method:** DELETE
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Delete task

##### 🟢 **TaskToggleCompleteView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** IsAuthenticated + IsOwner
- **Logic:**
  - Toggle task status between 'completed' and 'todo'
  - If completing: set completed_at = now
  - If uncompleting: set completed_at = None
  - Return updated task

##### 🟢 **TaskArchiveView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** IsAuthenticated + IsOwner
- **Logic:**
  - Set task status to 'archived'
  - Return success message

##### 🟢 **BulkCompleteTasksView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Logic:**
  - Accept list of task IDs
  - Verify all tasks belong to user
  - Mark all as completed
  - Set completed_at for all
  - Return count of updated tasks

---

#### **Analytics/Dashboard Views**

##### 🟢 **TaskStatisticsView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Calculate total tasks
  - Count by status (todo, in_progress, completed, archived)
  - Count completed today
  - Count overdue tasks (due_date < today && status != completed)
  - Count high/urgent priority tasks
  - Calculate completion rate
  - Return JSON statistics

##### 🟢 **OverdueTasksView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Filter tasks: due_date < today AND status != 'completed'
  - Order by due_date (oldest first)
  - Return overdue tasks list

##### 🟢 **TodayTasksView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Filter tasks: due_date = today
  - Exclude archived
  - Order by priority
  - Return today's tasks

---

### 🌟 What Makes It Resume-Worthy?
✅ Full CRUD operations  
✅ JWT Authentication  
✅ Custom permissions  
✅ Advanced filtering & search  
✅ Business logic (statistics, reminders)  
✅ Clean API design  
✅ Relational database design  

---

## 📌 Project 2: Expense Tracker API

### 🎯 Why This Project?
- **Practical Application**: Personal finance management
- **Data Analytics**: Shows you can handle calculations and aggregations
- **Date Handling**: Demonstrates time-based queries
- **Perfect for Demos**: Easy to show with real data

### 📱 Project Overview
A personal expense tracking API where users can record their income and expenses, categorize them, set budgets, and get spending insights.

### 🏗️ App Structure
**Single App:** `finance`

**User Role:** `Regular User` (manages their own finances)

### 📊 Models

#### **CustomUser Model**
- email, username
- monthly_budget (DecimalField, optional)
- currency (CharField, default='PKR')

#### **Category Model**
- user (ForeignKey)
- name (CharField: e.g., 'Food', 'Transport', 'Shopping')
- type (CharField: choices - 'income', 'expense')
- icon (CharField)
- color (CharField)
- monthly_budget (DecimalField, optional - budget per category)

#### **Transaction Model**
- user (ForeignKey)
- category (ForeignKey to Category)
- amount (DecimalField)
- type (CharField: 'income' or 'expense')
- description (TextField)
- date (DateField)
- payment_method (CharField: choices - 'cash', 'card', 'bank_transfer', 'mobile_wallet')
- is_recurring (BooleanField)
- created_at

#### **Budget Model** (Optional)
- user (ForeignKey)
- category (ForeignKey to Category, optional)
- amount (DecimalField)
- month (DateField)
- created_at

### 🎯 Views Structure (CRUD vs Logical)

> **Legend:** 🔵 = CRUD View | 🟢 = Logical View

#### **Authentication Views**
Same as Task Management (Registration, Login, Logout, Profile)

---

#### **Category Views**

##### 🔵 **CategoryListCreateView** (CRUD - ListCreateAPIView)
- **Methods:** GET, POST
- **Permission:** IsAuthenticated
- **Filtering:** `type` (income or expense)
- **Description:** List and create user's income/expense categories

##### 🔵 **CategoryDetailView** (CRUD - RetrieveUpdateDestroyAPIView)
- **Methods:** GET, PUT, PATCH, DELETE
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Manage specific category

---

#### **Transaction Views**

##### 🔵 **TransactionListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Filtering:**
  - `type` (income or expense)
  - `category` (by category ID)
  - `payment_method` (cash, card, bank_transfer, mobile_wallet)
  - `date` (exact date)
  - `date_from` & `date_to` (date range)
  - `month` (specific month YYYY-MM)
  - `search` (description)
- **Ordering:** -date, amount, -created_at
- **Pagination:** PageNumberPagination (25 per page)
- **Description:** List all user's transactions

##### 🔵 **TransactionCreateView** (CRUD - CreateAPIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Description:** Add new income/expense transaction

##### 🔵 **TransactionDetailView** (CRUD - RetrieveAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Get transaction details

##### 🔵 **TransactionUpdateView** (CRUD - UpdateAPIView)
- **Methods:** PUT, PATCH
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Update transaction

##### 🔵 **TransactionDeleteView** (CRUD - DestroyAPIView)
- **Method:** DELETE
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Delete transaction

---

#### **Analytics/Dashboard Views**

##### 🟢 **DashboardView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Calculate total income (all time)
  - Calculate total expenses (all time)
  - Calculate current balance (income - expenses)
  - Calculate savings rate percentage
  - Count total transactions
  - Get current month income vs expenses
  - Return dashboard statistics

##### 🟢 **MonthlyReportView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Query Params:** `month` (YYYY-MM, optional, default=current)
- **Logic:**
  - Filter transactions by specified month
  - Calculate total income for month
  - Calculate total expenses for month
  - Calculate net savings
  - Group by category with totals
  - Return monthly breakdown

##### 🟢 **CategoryBreakdownView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Query Params:** `month` (optional), `type` (income/expense)
- **Logic:**
  - Group transactions by category
  - Calculate sum for each category
  - Calculate percentage of total
  - Return data suitable for pie chart

##### 🟢 **TrendAnalysisView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Query Params:** `months` (default=6)
- **Logic:**
  - Get last N months data
  - Calculate income and expenses per month
  - Calculate monthly savings
  - Return time-series data for line chart

##### 🟢 **BudgetAlertsView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Get all categories with budget set
  - Calculate current month spending per category
  - Compare with budget limit
  - Flag categories exceeding budget
  - Return list of budget alerts with percentage used

##### 🟢 **TopSpendingCategoriesView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Query Params:** `limit` (default=5), `month` (optional)
- **Logic:**
  - Group expense transactions by category
  - Order by total amount (descending)
  - Return top N categories

---

### 🌟 What Makes It Resume-Worthy?
✅ Complex aggregations (SUM, AVG, GROUP BY)  
✅ Date-based filtering and analytics  
✅ Data visualization endpoints  
✅ Budget management logic  
✅ Financial calculations  
✅ Real-world problem solving  

---

## 📌 Project 3: Blog API with Social Features

### 🎯 Why This Project?
- **Content Management**: Shows CRUD expertise
- **Social Features**: Likes, comments, follows
- **File Uploads**: Image handling for posts
- **SEO-friendly**: Slug-based URLs

### 📱 Project Overview
A blogging platform API where users can write articles, upload images, interact with other posts through likes and comments, and follow their favorite authors.

### 🏗️ App Structure
**Single App:** `blog`

**User Role:** `Author` (creates and manages blog posts)

### 📊 Models

#### **CustomUser Model**
- email, username
- bio (TextField)
- profile_picture (ImageField)
- website (URLField, optional)
- followers_count (IntegerField, default=0)
- following_count (IntegerField, default=0)

#### **Category Model**
- name (CharField, unique)
- slug (SlugField)
- description (TextField)

#### **Tag Model**
- name (CharField, unique)
- slug (SlugField)

#### **Post Model**
- author (ForeignKey to User)
- title (CharField)
- slug (SlugField, unique)
- content (TextField)
- excerpt (TextField - short description)
- featured_image (ImageField, optional)
- category (ForeignKey to Category)
- tags (ManyToManyField to Tag)
- status (CharField: choices - 'draft', 'published')
- views_count (IntegerField, default=0)
- likes_count (IntegerField, default=0)
- comments_count (IntegerField, default=0)
- is_featured (BooleanField)
- published_at (DateTimeField, null)
- created_at
- updated_at

#### **Comment Model**
- post (ForeignKey to Post)
- user (ForeignKey to User)
- content (TextField)
- parent (ForeignKey to self, null - for nested comments)
- created_at
- updated_at

#### **Like Model**
- user (ForeignKey to User)
- post (ForeignKey to Post)
- created_at
- **Unique Together**: user + post (one like per user per post)

#### **Follow Model**
- follower (ForeignKey to User)
- following (ForeignKey to User)
- created_at
- **Unique Together**: follower + following

### 🎯 Views Structure (CRUD vs Logical)

> **Legend:** 🔵 = CRUD View | 🟢 = Logical View

#### **Authentication Views**
Same as previous projects

---

#### **Category & Tag Views**

##### 🔵 **CategoryListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Description:** List all categories

##### 🔵 **TagListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Description:** List all tags

##### 🟢 **TagCloudView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** AllowAny
- **Logic:**
  - Get all tags with post count
  - Calculate popularity weight
  - Return tags with usage count

---

#### **Post Views**

##### 🔵 **PostListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Filtering:**
  - `status` (published only for non-authors)
  - `category` (by category slug)
  - `tag` (by tag slug)
  - `author` (by author username)
  - `is_featured` (boolean)
  - `search` (title, content, excerpt)
- **Ordering:** -published_at, -views_count, -likes_count, -created_at
- **Pagination:** PageNumberPagination (10 per page)
- **Description:** List published posts

##### 🔵 **PostCreateView** (CRUD - CreateAPIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Description:** Create new post (draft or published)

##### 🟢 **PostDetailView** (LOGICAL - RetrieveAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Logic:**
  - Get post by slug
  - Increment view count automatically
  - Return post with author details, comments count, likes count

##### 🔵 **PostUpdateView** (CRUD - UpdateAPIView)
- **Methods:** PUT, PATCH
- **Permission:** IsAuthenticated + IsAuthor
- **Description:** Update own post

##### 🔵 **PostDeleteView** (CRUD - DestroyAPIView)
- **Method:** DELETE
- **Permission:** IsAuthenticated + IsAuthor
- **Description:** Delete own post

##### 🟢 **MyPostsView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Filtering:** `status` (draft or published)
- **Logic:**
  - Filter posts by current user
  - Show both drafts and published
  - Return user's posts

---

#### **Social Feature Views**

##### 🟢 **PostLikeToggleView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Logic:**
  - Check if user already liked post
  - If liked: Unlike (delete Like object, decrement likes_count)
  - If not liked: Like (create Like object, increment likes_count)
  - Return is_liked status and new likes_count

##### 🔵 **CommentListCreateView** (CRUD - ListCreateAPIView)
- **Methods:** GET, POST
- **Permission:** AllowAny (GET), IsAuthenticated (POST)
- **Filtering:** `post` (by post slug or ID)
- **Description:** List and create comments for a post

##### 🔵 **CommentUpdateView** (CRUD - UpdateAPIView)
- **Methods:** PUT, PATCH
- **Permission:** IsAuthenticated + IsCommentOwner
- **Description:** Update own comment

##### 🔵 **CommentDeleteView** (CRUD - DestroyAPIView)
- **Method:** DELETE
- **Permission:** IsAuthenticated + IsCommentOwner
- **Description:** Delete own comment

##### 🟢 **FollowToggleView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Logic:**
  - Accept target user_id
  - Check if already following
  - If following: Unfollow (delete Follow, update counts)
  - If not: Follow (create Follow, update counts)
  - Return is_following status

##### 🟢 **UserFeedView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Get all users current user is following
  - Get published posts from these authors
  - Order by -published_at
  - Return personalized feed

---

#### **Discovery Views**

##### 🟢 **TrendingPostsView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Logic:**
  - Filter posts from last 7 days
  - Order by likes_count + views_count (weighted)
  - Limit to top 10
  - Return trending posts

##### 🟢 **RelatedPostsView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Query Params:** `post_slug` (required)
- **Logic:**
  - Get current post's tags
  - Find other posts with similar tags
  - Exclude current post
  - Order by matching tags count
  - Limit to 5
  - Return related posts

##### 🟢 **AuthorProfileView** (LOGICAL - RetrieveAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Logic:**
  - Get author details
  - Count total posts (published)
  - Get followers count
  - Get following count
  - Return author profile with stats

---

### 🌟 What Makes It Resume-Worthy?
✅ Content management system  
✅ Many-to-Many relationships  
✅ Social interaction logic  
✅ File/Image uploads  
✅ SEO optimization (slugs)  
✅ Complex queries (feeds, trending)  
✅ Nested comments (recursive relationships)  

---

## 📌 Project 4: Fitness Tracker API

### 🎯 Why This Project?
- **Health Tech**: Trending industry
- **Data Tracking**: Shows time-series data handling
- **Goal Management**: User motivation features
- **Charts & Analytics**: Great for data visualization

### 📱 Project Overview
A personal fitness tracking API where users can log workouts, track nutrition, set fitness goals, monitor progress, and view their health statistics.

### 🏗️ App Structure
**Single App:** `fitness`

**User Role:** `Regular User` (tracks their fitness journey)

### 📊 Models

#### **CustomUser Model**
- email, username
- age (IntegerField)
- gender (CharField)
- height (DecimalField - in cm)
- current_weight (DecimalField)
- target_weight (DecimalField, optional)
- fitness_goal (CharField: choices - 'lose_weight', 'gain_muscle', 'maintain', 'improve_endurance')

#### **Exercise Model**
- name (CharField: e.g., 'Running', 'Push-ups')
- category (CharField: choices - 'cardio', 'strength', 'flexibility', 'sports')
- calories_per_minute (DecimalField, optional)
- description (TextField)

#### **Workout Model**
- user (ForeignKey)
- exercise (ForeignKey to Exercise)
- date (DateField)
- duration (IntegerField - in minutes)
- calories_burned (DecimalField)
- distance (DecimalField, optional - for running/cycling)
- reps (IntegerField, optional - for strength training)
- sets (IntegerField, optional)
- notes (TextField, optional)
- created_at

#### **WeightLog Model**
- user (ForeignKey)
- weight (DecimalField)
- date (DateField)
- notes (TextField, optional)

#### **NutritionLog Model**
- user (ForeignKey)
- meal_type (CharField: choices - 'breakfast', 'lunch', 'dinner', 'snack')
- food_name (CharField)
- calories (IntegerField)
- protein (DecimalField, optional - in grams)
- carbs (DecimalField, optional)
- fats (DecimalField, optional)
- date (DateField)
- created_at

#### **Goal Model**
- user (ForeignKey)
- goal_type (CharField: choices - 'weight_loss', 'workout_frequency', 'calories_burn')
- target_value (DecimalField)
- current_value (DecimalField, default=0)
- deadline (DateField)
- status (CharField: choices - 'active', 'achieved', 'abandoned')
- created_at

### 🎯 Views Structure (CRUD vs Logical)

> **Legend:** 🔵 = CRUD View | 🟢 = Logical View

#### **Authentication Views**
Same as previous projects (with fitness profile data)

---

#### **Exercise Management Views**

##### 🔵 **ExerciseListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Filtering:** `category` (cardio, strength, flexibility, sports)
- **Description:** List all available exercises

---

#### **Workout Views**

##### 🔵 **WorkoutListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Filtering:**
  - `date` (specific date)
  - `date_from` & `date_to` (date range)
  - `exercise` (by exercise ID)
  - `category` (cardio, strength, etc.)
- **Ordering:** -date, -created_at, duration
- **Pagination:** PageNumberPagination (20 per page)
- **Description:** List user's workout history

##### 🔵 **WorkoutCreateView** (CRUD - CreateAPIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Description:** Log new workout session

##### 🔵 **WorkoutDetailView** (CRUD - RetrieveAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Get workout details

##### 🔵 **WorkoutUpdateView** (CRUD - UpdateAPIView)
- **Methods:** PUT, PATCH
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Update workout entry

##### 🔵 **WorkoutDeleteView** (CRUD - DestroyAPIView)
- **Method:** DELETE
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Delete workout entry

##### 🟢 **WorkoutSummaryView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Query Params:** `date_from`, `date_to` (optional)
- **Logic:**
  - Calculate total workouts in period
  - Sum total duration (minutes)
  - Sum total calories burned
  - Sum total distance (if applicable)
  - Return workout summary statistics

---

#### **Weight Tracking Views**

##### 🔵 **WeightLogListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Ordering:** -date
- **Description:** List user's weight history

##### 🔵 **WeightLogCreateView** (CRUD - CreateAPIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Description:** Log current weight

##### 🟢 **WeightProgressView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Get current weight (latest log)
  - Get target weight from user profile
  - Calculate starting weight (oldest log)
  - Calculate weight lost/gained
  - Calculate progress percentage
  - Return weight progress data

##### 🟢 **WeightChartView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Query Params:** `days` (default=30)
- **Logic:**
  - Get weight logs for last N days
  - Format for line chart (date, weight pairs)
  - Return chart data

---

#### **Nutrition Views**

##### 🔵 **NutritionLogListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Filtering:**
  - `date` (specific date)
  - `meal_type` (breakfast, lunch, dinner, snack)
- **Ordering:** -date, -created_at
- **Description:** List user's nutrition logs

##### 🔵 **NutritionLogCreateView** (CRUD - CreateAPIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Description:** Log meal/food intake

##### 🟢 **DailyNutritionSummaryView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Query Params:** `date` (default=today)
- **Logic:**
  - Get all nutrition logs for date
  - Sum total calories consumed
  - Sum total protein, carbs, fats
  - Get calories burned from workouts
  - Calculate net calories (consumed - burned)
  - Return daily nutrition summary

---

#### **Goal Management Views**

##### 🔵 **GoalListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Filtering:** `status` (active, achieved, abandoned)
- **Description:** List user's fitness goals

##### 🔵 **GoalCreateView** (CRUD - CreateAPIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Description:** Set new fitness goal

##### 🔵 **GoalUpdateView** (CRUD - UpdateAPIView)
- **Methods:** PUT, PATCH
- **Permission:** IsAuthenticated + IsOwner
- **Description:** Update goal progress

##### 🟢 **GoalMarkAchievedView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** IsAuthenticated + IsOwner
- **Logic:**
  - Check if target value reached
  - Set status to 'achieved'
  - Set achievement date
  - Return success message with congratulations

---

#### **Analytics/Dashboard Views**

##### 🟢 **DashboardView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Get today's total calories burned
  - Get today's workouts count
  - Get today's nutrition (calories consumed)
  - Get current weight vs target
  - Get active goals count
  - Get current workout streak
  - Return comprehensive dashboard

##### 🟢 **WeeklyReportView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Get last 7 days workouts
  - Calculate total workouts
  - Calculate total calories burned
  - Calculate average duration per workout
  - Calculate total distance
  - Group by exercise category
  - Return weekly statistics

##### 🟢 **WorkoutStreakView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Get all workout dates
  - Calculate consecutive workout days
  - Calculate current streak
  - Calculate longest streak ever
  - Return streak statistics

##### 🟢 **ActivityHeatmapView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Query Params:** `year` (default=current year)
- **Logic:**
  - Get all workout dates for year
  - Format data for calendar heatmap
  - Include workout count per day
  - Return calendar data (365 days)

##### 🟢 **AchievementsView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Check milestones (10 workouts, 50 workouts, 100 workouts)
  - Check weight milestones
  - Check streak milestones
  - Return list of unlocked achievements

---

### 🌟 What Makes It Resume-Worthy?
✅ Health/fitness domain (trending)  
✅ Time-series data handling  
✅ Complex analytics and aggregations  
✅ Goal tracking logic  
✅ Progress monitoring  
✅ Data for visualization  
✅ User motivation features  

---

## 📌 Project 5: Event Management & Booking API

### 🎯 Why This Project?
- **Booking System**: Real business logic
- **Date/Time Management**: Advanced datetime handling
- **Capacity Management**: Seat availability logic
- **Transaction-like Operations**: Booking confirmations

### 📱 Project Overview
An event management API where users can browse events, book tickets, manage their bookings, receive confirmations, and organizers can create and manage events.

### 🏗️ App Structure
**Single App:** `events`

**User Roles:** `Attendee` (books events) + `Organizer` (creates events)

> **Note:** This has 2 user roles, but you can simplify to just Attendee role if needed

### 📊 Models

#### **CustomUser Model**
- email, username
- phone_number
- role (CharField: choices - 'attendee', 'organizer')
- is_verified (BooleanField)

#### **Category Model**
- name (CharField: e.g., 'Tech', 'Music', 'Sports')
- slug (SlugField)

#### **Event Model**
- organizer (ForeignKey to User)
- title (CharField)
- slug (SlugField)
- description (TextField)
- category (ForeignKey to Category)
- event_type (CharField: choices - 'online', 'offline')
- venue (CharField, optional for online)
- address (TextField)
- city (CharField)
- start_datetime (DateTimeField)
- end_datetime (DateTimeField)
- total_seats (IntegerField)
- available_seats (IntegerField)
- price (DecimalField, 0 for free events)
- banner_image (ImageField, optional)
- status (CharField: choices - 'upcoming', 'ongoing', 'completed', 'cancelled')
- is_featured (BooleanField)
- created_at
- updated_at

#### **Booking Model**
- user (ForeignKey to User)
- event (ForeignKey to Event)
- booking_number (CharField, unique, auto-generated)
- number_of_seats (IntegerField)
- total_amount (DecimalField)
- status (CharField: choices - 'pending', 'confirmed', 'cancelled')
- payment_status (CharField: choices - 'pending', 'paid', 'refunded')
- booking_date (DateTimeField)
- created_at

**Unique Together:** Prevent duplicate active bookings

#### **Review Model** (Optional)
- user (ForeignKey)
- event (ForeignKey)
- rating (IntegerField, 1-5)
- comment (TextField)
- created_at

### 🎯 Views Structure (CRUD vs Logical)

> **Legend:** 🔵 = CRUD View | 🟢 = Logical View

#### **Authentication Views**
Same as previous projects (with role selection)

---

#### **Category Views**

##### 🔵 **CategoryListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Description:** List all event categories

---

#### **Event Views (Public)**

##### 🔵 **EventListView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Filtering:**
  - `category` (by category slug)
  - `city` (by city name)
  - `event_type` (online or offline)
  - `status` (upcoming only for public)
  - `price_min` & `price_max` (price range)
  - `date_from` & `date_to` (date range)
  - `is_featured` (boolean)
  - `search` (title, description)
- **Ordering:** start_datetime, -created_at, price
- **Pagination:** PageNumberPagination (12 per page)
- **Description:** List all public upcoming events

##### 🟢 **EventDetailView** (LOGICAL - RetrieveAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Logic:**
  - Get event by slug
  - Calculate available seats percentage
  - Check if event is sold out
  - Check if user has booked (if authenticated)
  - Return event with real-time availability

##### 🟢 **FeaturedEventsView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Logic:**
  - Filter is_featured=True
  - Filter upcoming events only
  - Order by start_datetime
  - Limit to 6 events
  - Return featured events

##### 🟢 **PopularEventsView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** AllowAny
- **Logic:**
  - Count bookings per event
  - Order by booking count (descending)
  - Filter upcoming events
  - Limit to 10
  - Return most popular events

---

#### **Event Views (Organizer)**

##### 🔵 **EventCreateView** (CRUD - CreateAPIView)
- **Method:** POST
- **Permission:** IsAuthenticated + IsOrganizer
- **Description:** Create new event (auto-set organizer as current user)

##### 🔵 **EventUpdateView** (CRUD - UpdateAPIView)
- **Methods:** PUT, PATCH
- **Permission:** IsAuthenticated + IsEventOrganizer
- **Description:** Update own event details

##### 🟢 **EventCancelView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** IsAuthenticated + IsEventOrganizer
- **Logic:**
  - Set event status to 'cancelled'
  - Get all bookings for event
  - Cancel all bookings
  - Send cancellation emails
  - Return success message

##### 🟢 **MyEventsView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated + IsOrganizer
- **Filtering:** `status` (upcoming, ongoing, completed, cancelled)
- **Logic:**
  - Filter events by current organizer
  - Return organizer's events

##### 🟢 **EventBookingsView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated + IsEventOrganizer
- **Logic:**
  - Get all bookings for organizer's event
  - Show booking details with user info
  - Return event bookings list

##### 🟢 **EventStatisticsView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated + IsEventOrganizer
- **Logic:**
  - Count total bookings
  - Calculate total revenue
  - Calculate seats sold percentage
  - Count confirmed vs pending bookings
  - Return event statistics

---

#### **Booking Views (Attendee)**

##### 🟢 **BookingCreateView** (LOGICAL - CreateAPIView)
- **Method:** POST
- **Permission:** IsAuthenticated
- **Logic:**
  - Validate event exists and is upcoming
  - Check seat availability (available_seats >= requested)
  - Generate unique booking number
  - Calculate total amount
  - Deduct seats from available_seats (atomic)
  - Create booking with 'pending' status
  - Send booking confirmation email
  - Return booking details

##### 🔵 **MyBookingsView** (CRUD - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Filtering:**
  - `status` (pending, confirmed, cancelled)
  - `upcoming` (boolean - future events only)
- **Ordering:** -booking_date
- **Description:** List user's all bookings

##### 🔵 **BookingDetailView** (CRUD - RetrieveAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated + IsBookingOwner
- **Description:** Get booking details with QR code

##### 🟢 **BookingCancelView** (LOGICAL - APIView)
- **Method:** POST
- **Permission:** IsAuthenticated + IsBookingOwner
- **Logic:**
  - Check event hasn't started yet
  - Set booking status to 'cancelled'
  - Restore seats (add back to available_seats)
  - Process refund if paid
  - Send cancellation confirmation email
  - Return success message

---

#### **Advanced Views**

##### 🟢 **CheckAvailabilityView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** AllowAny
- **Query Params:** `event_id`, `seats` (number of seats to check)
- **Logic:**
  - Get event's current available_seats
  - Check if requested seats <= available
  - Return availability status (boolean)

##### 🟢 **UpcomingEventsReminderView** (LOGICAL - ListAPIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Get user's confirmed bookings
  - Filter events starting in next 7 days
  - Order by start_datetime
  - Return upcoming events with reminder

##### 🟢 **UserBookingHistoryView** (LOGICAL - APIView)
- **Method:** GET
- **Permission:** IsAuthenticated
- **Logic:**
  - Count total bookings
  - Count attended events (completed)
  - Count cancelled bookings
  - Calculate total spent
  - Get favorite category (most booked)
  - Return booking analytics

---

### 🌟 What Makes It Resume-Worthy?
✅ Complex booking logic  
✅ Inventory management (seats)  
✅ Transaction safety (atomicity)  
✅ Multiple user roles (if included)  
✅ Real-world business problem  
✅ Date/time handling  
✅ Booking system experience  

---

## 🎖️ **Recommendation for YOUR Resume:**

### **Best Choice: Task Management API** ⭐

**Why?**
1. ✅ **Perfect Complexity**: Not too simple, not too complex
2. ✅ **Easy to Explain**: Everyone understands task management
3. ✅ **Quick to Build**: Can complete in 1-2 weeks
4. ✅ **Demo-Friendly**: Easy to show in interviews
5. ✅ **Shows Core Skills**: CRUD, Auth, Permissions, Filtering
6. ✅ **Add Advanced Features Easily**: Statistics, reminders, bulk operations

### **Alternative Choice: Fitness Tracker API** 🏃

**Why?**
1. ✅ **Trending Domain**: Health tech is hot
2. ✅ **Data Analytics**: Shows you can handle complex queries
3. ✅ **Unique**: Less common than task managers
4. ✅ **Chart-Friendly**: Great for frontend integration demos
5. ✅ **Personal Touch**: You can actually use it!

---

## 📝 **Implementation Tips for Resume Impact:**

### 1. **Code Quality**
- Use proper naming conventions
- Add docstrings to all classes and methods
- Follow DRF best practices
- Use serializers properly

### 2. **Documentation**
- Create detailed README with setup instructions
- Document all API endpoints (use drf-spectacular)
- Add Postman collection
- Include API documentation (Swagger)

### 3. **Best Practices**
- JWT Authentication
- Custom permissions
- Pagination on all list endpoints
- Filtering with django-filter
- Search functionality
- Proper error handling
- Input validation

### 4. **Testing**
- Write API tests for main endpoints
- Test permissions
- Test edge cases

### 5. **Deployment** (Huge Resume Boost!)
- Deploy on Heroku/Railway (free)
- Add live API URL to resume
- Make it accessible for recruiters to test

### 6. **GitHub Repository**
- Clear README
- Requirements.txt
- .env.example file
- Proper .gitignore
- Clean commit history
- Add screenshots or GIF demos

---

## 🚀 **What to Mention on Resume:**

```
Task Management API | Django REST Framework
- Built RESTful API with JWT authentication serving 15+ endpoints
- Implemented advanced filtering, search, and pagination using django-filter
- Created custom permissions for resource-level access control
- Developed analytics endpoints for task statistics and productivity insights
- Designed relational database schema with optimized queries
- Deployed on Heroku with PostgreSQL database
Technologies: Django, DRF, PostgreSQL, JWT, Docker (optional)
```

---

## ✨ **Final Advice:**

1. **Pick ONE project** and make it excellent rather than multiple mediocre ones
2. **Add 3-4 advanced features** from the suggestions to stand out
3. **Deploy it live** - having a working URL is 10x more impressive
4. **Write good documentation** - README is as important as code
5. **Show data** - Add sample data/fixtures for demos
6. **Test thoroughly** - Make sure everything works perfectly

**Good luck with your internship applications! 🎯**
